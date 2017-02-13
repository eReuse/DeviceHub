from collections import Iterable
from collections import defaultdict

from bson import ObjectId
from passlib.utils import classproperty
from pydash import pick
from pymongo.errors import OperationFailure

from ereuse_devicehub.exceptions import StandardError
from ereuse_devicehub.resources.device.component.domain import ComponentDomain
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.domain import Domain, ResourceNotFound
from ereuse_devicehub.resources.group.abstract.lot.settings import Lot
from ereuse_devicehub.resources.group.physical.package.settings import Package
from ereuse_devicehub.resources.group.physical.place.settings import Place
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

        for name in cls.children_resources.keys():
            resource_original = set(original[name]) if name in original else set()
            resource_updated = set(updated[name]) if name in updated else set()
            new_orphans = resource_original - resource_updated
            new_adopted = resource_updated - resource_original

            if name == Device.resource_name:  # We get the components of devices
                new_orphans |= ComponentDomain.get_components_in_set(list(new_orphans))
                new_adopted |= ComponentDomain.get_components_in_set(list(new_adopted))

            child_domain = cls.children_resources[name]
            # We remove our foreign key (with our ancestors) in the orphans' documents
            cls.disinherit(label, child_domain, new_orphans)

            # We remove other parents (some groups may override it and do nothing here)
            cls.remove_other_parents_of_type(child_domain, new_adopted)

            # We add our foreign key (with our ancestors) in the new adopted's documents
            cls.inherit(label, ancestors, child_domain, new_adopted)

    @classmethod
    def disinherit(cls, parent_label: str, child_domain: Domain, children: Iterable):
        """
        Removes the *ancestors* dict the children inherited from the parent, and then recursively updates
        the ancestors of the descendants of the children.

        :param parent_label: The label of the parent, used as FK.
        :param child_domain: The domain of the children. Note that this forces all children to be of the same @type.
        Call inherit as many times as types of children you have.
        :param children: A list of children labels.
        """

        q = {'$pull': {'ancestors': {'@type': cls.resource_settings._schema.type_name, 'label': parent_label}}}
        full_children = child_domain.update_raw_get(children, q)
        if issubclass(child_domain, GroupDomain):
            cls._update_inheritance_grandchildren(full_children, child_domain)

    @classmethod
    def remove_other_parents_of_type(cls, child_domain: Domain, children: Iterable):
        """
        Removes any parent of the same type of the parent children have.

        By default a resource can only have one parent of a type, so we remove another parent of the same
        type that our children have. Some groups like lots of packages *share parenthood* (they allow
        multiple parents simultaniously for their children) and they override this method with a *pass*.

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
        groups = (Place.resource_name, Package.resource_name, Lot.resource_name, Device.resource_name)
        full_children = cls._inherit(groups, parent_label, parent_ancestors, child_domain, children)
        if issubclass(child_domain, GroupDomain):
            cls._update_inheritance_grandchildren(full_children, child_domain)

    @classmethod
    def _inherit(cls, groups_to_inherit: Iterable, parent_label: str, parent_ancestors: list, child_domain: Domain,
                 children: Iterable):
        """
        Copies the passed-in ancestors to the children.

        Ancestors are merged in a set, avoiding repetition of ancestors for resources with multiple parents.

        When pasting the copy, it tries to identify an existing ancestors dictionary given by the parent,
        otherwise creates a new one.
        """
        child_ancestors = defaultdict(set)
        child_ancestors['@type'] = cls.resource_settings._schema.type_name
        child_ancestors['label'] = parent_label
        for parent_parent in parent_ancestors:
            for resource_name in groups_to_inherit:
                if resource_name in parent_parent:
                    child_ancestors[resource_name] |= set(parent_parent[resource_name])
                if parent_parent['@type'] == Naming.type(resource_name):  # We add the parent's parent
                    child_ancestors[resource_name].add(parent_parent['@type'])
        # Let's try to update an existing ancestor dict (this is with the same label and @type),
        # Note that this only will succeed when a relationship child-parent already exists, and this case happens
        # when we are updating the grandchilden (and so on) after adding/deleting a relationship
        try:
            extra_query = {'ancestors.@type': child_ancestors['@type'], 'ancestors.label': child_ancestors['label']}
            update_query = {'$set': {}}
            for key, value in pick(child_ancestors, groups_to_inherit):
                update_query['$set']['ancestors.$.' + key] = value
            return child_domain.update_raw_get(children, update_query, extra_query=extra_query)
        except OperationFailure as e:
            if e.code == 16836:
                # There is not an ancestor dict, so let's create one
                # This only happens when creating a relationship parent-child
                update_query = {'$push': {'ancestors': {'$each': [child_ancestors], '$position': 0}}}
                return child_domain.update_raw_get(children, update_query)
            else:
                raise e

    @classmethod
    def _update_inheritance_grandchildren(cls, full_children: list, child_domain: 'GroupDomain'):
        """
        Moves forward in updating the inheritance for the descendants by calling inherit, passing the
        child as the parent and the grand-children as children.

        As *inherit* calls this method, recursively they update the ancestors of all descendants.
        :param full_children: The children whose children (our grand-children) will be updated
        :param child_domain: The domain of the children. Note that this forces all children to be the same @type.
        """
        if child_domain.resource_settings.resource_name() in Group.types:
            for full_child in full_children:
                for name in child_domain.children_resources.keys():
                    grandchildren_domain = child_domain.children_resources[name]
                    grandchildren = set(full_child['children'][name]) if name in full_child['children'] else set()
                    child_domain.inherit(full_child['label'], full_child['ancestors'], grandchildren_domain,
                                         grandchildren)

    @classproperty
    def children_resources(cls):
        if not hasattr(cls, '_children_resources'):
            from ereuse_devicehub.resources.group.physical.place.domain import PlaceDomain
            from ereuse_devicehub.resources.group.physical.package.domain import PackageDomain
            from ereuse_devicehub.resources.group.abstract.lot.domain import LotDomain
            cls._children_resources = {
                Place.resource_name: PlaceDomain,
                Package.resource_name: PackageDomain,
                Device.resource_name: DeviceDomain,
                Lot.resource_name: LotDomain,
                Place.type_name: PlaceDomain,
                Package.type_name: PackageDomain,
                Device.type_name: DeviceDomain,
                Lot.type_name: LotDomain
            }
        return cls._children_resources

    @classmethod
    def is_parent(cls, parent_type: str, parent_label: str, child_label: str) -> bool:
        q = {'label': child_label, 'ancestors': {'$elemMatch': {'@type': parent_type, 'label': parent_label}}}
        try:
            return bool(cls.get_one(q))
        except ResourceNotFound:
            return False

    @classmethod
    def is_ancestor(cls, ancestor_resource_name: str, ancestor_label: str, descendant_label: str) -> bool:
        """
        Checks if *ancestor_label* is an ancestor of *descendant_label*.

        This is possible because during the inheritance, we only add to 'ancestors' the valid ones.

        """
        query = {
            'label': descendant_label,
            '$or': [
                {'ancestors.@type': Naming.type(ancestor_resource_name), 'label': ancestor_label},  # is parent
                {'ancestors': {'$elemMatch': {ancestor_resource_name: {'$elemMatch': ancestor_label}}}},  # >= grandpa
            ]
        }
        try:
            return bool(cls.get_one(query))
        except ResourceNotFound:
            return False

    @classmethod
    def update_raw(cls, ids: str or ObjectId or list, operation: dict, key='label'):
        """The same but updating 'label' per default"""
        return super().update_raw(ids, operation, key)

    @classmethod
    def update_one_raw(cls, resource_id: str or ObjectId, operation, key='label'):
        """The same but updating 'label' per default"""
        return super().update_one_raw(resource_id, operation, key)


class CannotDeleteIfHasEvent(StandardError):
    status_code = 400
    message = 'Delete all the events performed in the place before deleting the {} itself.'

    def __init__(self, resource_type):
        message = self.message.format(resource_type)
        super().__init__(message)
