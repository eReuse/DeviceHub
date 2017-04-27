from collections import Iterable

from bson import ObjectId
from passlib.utils import classproperty
from pydash import compact
from pydash import flatten
from pydash import map_values
from pydash import pick
from pydash import pluck
from pymongo import ReturnDocument
from pymongo.errors import OperationFailure

from ereuse_devicehub.resources.device.component.domain import ComponentDomain
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.domain import Domain, ResourceNotFound
from ereuse_devicehub.resources.group.settings import GroupSettings, Group
from ereuse_devicehub.utils import Naming


class GroupDomain(Domain):
    resource_settings = GroupSettings

    @classmethod
    def update_children(cls, original: dict, updated: dict, ancestors: list, label: str or None):
        """
        Updates the children of a group to reflect what says in the *original* field, materializing and affecting other
        resources.

        :param parent_name: The resource name of the parent.
        :param original: The original *children* field.
        :param updated: The new *children* field.
        :param ancestors: The *ancestors* field.
        :param label: The label of the group, used as an identifier.
        """

        for resource_name in cls.children_resources.keys():
            resource_original = set(original[resource_name]) if resource_name in original else set()
            resource_updated = set(updated[resource_name]) if resource_name in updated else set()
            new_orphans = resource_original - resource_updated
            new_adopted = resource_updated - resource_original

            if len(new_orphans) != 0 or len(new_adopted) != 0:
                cls._update_children(new_orphans, new_adopted, ancestors, resource_name, label)

    @classmethod
    def _update_children(cls, new_orphans: set, new_adopted: set, ancestors: list, resource_name: str,
                         label: str or None):
        child_domain = cls.children_resources[resource_name]
        # We remove our foreign key (with our ancestors) in the orphans' documents
        cls.disinherit(label, child_domain, new_orphans)

        # We remove other parents (some groups may override it and do nothing here)
        # Inherit, executed after, will propagate this changes to the descendants
        cls.remove_other_parents_of_type(child_domain, new_adopted)

        # We add our foreign key (with our ancestors) in the new adopted's documents
        # and we propagate all changes to our descendants
        cls.inherit(label, ancestors, child_domain, new_adopted)

    @classmethod
    def disinherit(cls, parent_label: str, child_domain: Domain, children: Iterable):
        """
        Removes the *ancestors* dict the children inherited from the parent, and then recursively updates
        the ancestors of the descendants of the children.
`
        :param parent_label: The label of the parent, used as FK.
        :param child_domain: The domain of the children. Note that this forces all children to be of the same @type.
        Call inherit as many times as types of children you have.
        :param children: A list of children labels.
        """
        q = {'$pull': {'ancestors': {'@type': cls.resource_settings._schema.type_name, 'label': parent_label}}}
        full_children = child_domain.update_raw_get(children, q)
        # We disinherit any component the devices have (only devices have components)
        # todo materialize 'components' field into group
        components = compact(flatten(pluck(full_children, 'components')))
        if len(components) > 0:
            cls.disinherit(parent_label, ComponentDomain, components)
        # Inherit children groups
        if issubclass(child_domain, GroupDomain):
            cls._update_inheritance_grandchildren(full_children, child_domain)

    @classmethod
    def remove_other_parents_of_type(cls, child_domain: Domain, children: Iterable):
        """
        Removes any parent of the same type of the parent children have.

        By default a resource can only have one parent of a type, so we remove another parent of the same
        type that our children have. Some groups like lots of packages *share parenthood* (they allow
        multiple parents simultaniously for their children) and they override this method with a *pass*.

        This method does not recursively update descendants –use **inherit() after**.

        :param child_domain: The domain of the children. Note that this forces all children to be of the same @type.
        Call inherit as many times as types of children you have.
        :param children: A list of children labels.
        """
        query = {'$pull': {'ancestors': {'@type': cls.resource_settings._schema.type_name}}}
        child_domain.update_raw(children, query)

    @classmethod
    def inherit(cls, parent_label: str, parent_ancestors: list, child_domain: Domain, children: Iterable):
        """
        Copies all the ancestors of the parent to the children (adding the parent as an ancestor), and then
        recursively updates the ancestors of the descendants of the children.

        Certain kind of groups behave differently here and they override this method.
        :param parent_label: The label of the parent, used as FK.
        :param parent_ancestors: An *ancestor dict*, see the Group Schema for more info.
        :param child_domain: The domain of the children. Note that this forces all children to be of the same @type.
        Call inherit as many times as types of children you have.
        :param children: A list of children labels.
        """
        # Inheritance mechanism:
        # - If parent is place, inherit all its places.
        #  - ancestors.prepend({'@type': 'Place', 'name': '', 'places': [label]})
        # - If parent is lot:
        #  - If child is lot, inherit places and lots
        #    - ancestors.prepend({'@type': 'Lot', 'name': '', 'places': [label], 'lots': [label]})
        #  - If child is package or device, inherit only lots
        #    - ancestors.prepend({'@type': 'Lot', 'name': '', 'lots': [label]})
        # - If parent is package (then child can only be package or device) inherit everything:
        #    - ancestors.prepend({'@type': 'Lot', 'name': '', 'lots': [label], 'packages': [label], 'places': [label]})

        # As places only have places is the same as inheriting everything they have.
        groups = cls.children_resources.keys()
        full_children = cls._inherit(groups, parent_label, parent_ancestors, child_domain, children)
        if issubclass(child_domain, GroupDomain):
            cls._update_inheritance_grandchildren(full_children, child_domain)

    @classmethod
    def _inherit(cls, groups_to_inherit: Iterable, parent_label: str, parent_ancestors: list, child_domain: Domain,
                 children: Iterable) -> list:
        """
        Copies the passed-in ancestors to the children.

        Ancestors are merged in a set, avoiding repetition of ancestors for resources with multiple parents.

        When pasting the copy, it tries to identify an existing ancestors dictionary given by the parent,
        otherwise creates a new one.
        """
        # The child_ancestors for the 'new' db query
        child_ancestors_new = {'@type': cls.resource_settings._schema.type_name, 'label': parent_label}
        # The child_ancestors for the 'update' db query
        child_ancestors_update = {'$set': {}}
        for resource_name in groups_to_inherit:
            child_ancestors_new[resource_name] = set()  # We want to explicitly 'set' for the db
            for grandparent in parent_ancestors:
                if resource_name in grandparent:
                    child_ancestors_new[resource_name] |= set(grandparent[resource_name])
                if grandparent['@type'] == Naming.type(resource_name):  # We add the grandparent itself
                    child_ancestors_new[resource_name].add(grandparent['label'])
            # Let's copy the result of the iteration to the update query
            child_ancestors_update['$set']['ancestors.$.' + resource_name] = child_ancestors_new[resource_name]
        return cls._update_db(parent_label, children, child_ancestors_new, child_ancestors_update, child_domain)

    @classmethod
    def _update_db(cls, parent_label: str, children: Iterable, ancestors_new: dict, ancestors_update: dict,
                   child_domain: Domain):
        new_children = []
        for child in children:  # We cannot run all the children at once when catching exceptions
            try:
                # Let's try to update an existing ancestor dict (this is with the same label and @type),
                # Note that this only will succeed when a relationship child-parent already exists, and this happens
                # when we are updating the grandchilden (and so on) after adding/deleting a relationship
                eq = {'ancestors.@type': ancestors_new['@type'], 'ancestors.label': parent_label}
                full_child, *_ = child_domain.update_raw_get(child, ancestors_update, extra_query=eq, upsert=True)

            except OperationFailure as e:
                if e.code == 16836:
                    # There is not an ancestor dict, so let's create one
                    # This only happens when creating a relationship parent-child
                    update_query = {'$push': {'ancestors': {'$each': [ancestors_new], '$position': 0}}}
                    full_child, *_ = child_domain.update_raw_get(child, update_query)
                else:
                    raise e
            if full_child is None:
                raise GroupNotFound('{} couldn\'t inheritance because it does not exist'.format(child))
            new_children.append(full_child)
            # todo materialize components
            components = full_child.get('components', [])  # Let's update the components
            cls._update_db(parent_label, components, ancestors_new, ancestors_update, ComponentDomain)
        return new_children

    @classmethod
    def _update_inheritance_grandchildren(cls, full_children: list, child_domain: 'GroupDomain'):
        """
        Moves forward in updating the inheritance for the descendants by calling inherit, passing the
        child as the parent and the grand-children as children.

        As *inherit* calls this method, recursively they update the ancestors of all descendants.
        :param full_children: The children whose children (our grand-children) will be updated
        :param child_domain: The domain of the children. Note that this forces all children to be the same @type.
        """
        if child_domain.resource_settings.resource_name() in Group.resource_types:
            for full_child in full_children:
                for name in child_domain.children_resources.keys():
                    grandchildren_domain = child_domain.children_resources[name]
                    grandchildren = set(full_child['children'][name]) if name in full_child['children'] else set()
                    if len(grandchildren) > 0:
                        child_domain.inherit(full_child['label'], full_child['ancestors'], grandchildren_domain,
                                             grandchildren)

    @classproperty
    def children_resources(cls):
        if not hasattr(cls, '_children_resources'):
            from ereuse_devicehub.resources.group.physical.place.domain import PlaceDomain
            from ereuse_devicehub.resources.group.physical.package.domain import PackageDomain
            from ereuse_devicehub.resources.group.abstract.lot.domain import LotDomain
            from ereuse_devicehub.resources.group.abstract.lot.incoming_lot.domain import IncomingLotDomain
            from ereuse_devicehub.resources.group.abstract.lot.outgoing_lot.domain import OutgoingLotDomain
            children_resources = {
                PlaceDomain.resource_settings.resource_name(): PlaceDomain,
                PackageDomain.resource_settings.resource_name(): PackageDomain,
                DeviceDomain.resource_settings.resource_name(): DeviceDomain,
                LotDomain.resource_settings.resource_name(): LotDomain,
                IncomingLotDomain.resource_settings.resource_name(): IncomingLotDomain,
                OutgoingLotDomain.resource_settings.resource_name(): OutgoingLotDomain,
                ComponentDomain.resource_settings.resource_name(): ComponentDomain,
            }
            types = {DeviceDomain.resource_settings.resource_name(), ComponentDomain.resource_settings.resource_name()}
            types |= cls.resource_settings._schema.resource_types
            cls._children_resources = pick(children_resources, *types)
        return cls._children_resources

    @classmethod
    def is_parent(cls, parent_type: str, parent_label: str, child_label: str) -> bool:
        q = {'label': child_label, 'ancestors': {'$elemMatch': {'@type': parent_type, 'label': parent_label}}}
        try:
            return bool(cls.get_one(q))
        except ResourceNotFound:
            return False

    @classmethod
    def get_descendants(cls, child_domain: Domain, parent_labels: str or list) -> list:
        """
        Get the descendants of this class type of the given ancestor.
        :param child_domain: The child domain.
        :param parent_labels: The label of a parent or a list of them. We retrieve descendants of **any** parent.
        """
        # The following is possible because during the inheritance, we only add to 'ancestors' the valid ones.
        type_name = cls.resource_settings._schema.type_name
        labels = parent_labels if type(parent_labels) is list else [parent_labels]
        query = {
            '$or': [
                {'ancestors': {'$elemMatch': {'@type': type_name, 'label': {'$in': labels}}}},
                {'ancestors': {'$elemMatch': {cls.resource_settings.resource_name(): {'$elemMatch': {'$in': labels}}}}}
            ]
        }
        return child_domain.get(query)

    @classmethod
    def get_all_descendants(cls, parent_labels: str or list) -> list:
        # Todo enhance by performing only one query
        return map_values(cls.children_resources, lambda domain: cls.get_descendants(domain, parent_labels))

    @classmethod
    def update_raw(cls, ids: str or ObjectId or list, operation: dict, key='label'):
        """The same but updating 'label' per default"""
        return super().update_raw(ids, operation, key)

    @classmethod
    def update_one_raw(cls, resource_id: str or ObjectId, operation, key='label'):
        """The same but updating 'label' per default"""
        return super().update_one_raw(resource_id, operation, key)

    @classmethod
    def update_raw_get(cls, ids: str or ObjectId or list, operation: dict, key='label',
                       return_document=ReturnDocument.AFTER, extra_query={}, **kwargs):
        return super().update_raw_get(ids, operation, key, return_document, extra_query, **kwargs)


class GroupNotFound(ResourceNotFound):
    pass
