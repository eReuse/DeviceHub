from collections import Iterable
from typing import Dict, List, Set, Type

from bson import ObjectId
from passlib.utils import classproperty
from pydash import compact, difference, union_by, difference_with, py_
from pydash import flatten
from pydash import map_values
from pydash import pick
from pydash import pluck
from pymongo.errors import OperationFailure

from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.device.component.domain import ComponentDomain
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.domain import Domain, ResourceNotFound
from ereuse_devicehub.resources.group.settings import GroupSettings, Group
from ereuse_devicehub.utils import Naming

Perms = List[Dict[str, str]]


# noinspection PyProtectedMember
class GroupDomain(Domain):
    resource_settings = GroupSettings

    @classmethod
    def update_children(cls, original: dict, updated: dict, ancestors: list, _id: str or None, perms: Perms):
        """
        Updates the children of a group to reflect what says in the *original* field, materializing and affecting other
        resources.

        :param original: The original *children* field.
        :param updated: The new *children* field.
        :param ancestors: The *ancestors* field.
        :param _id: The id of the group.
        :param perms: The *perms* field.
        """
        for resource_name in cls.children_resources.keys():
            resource_original = set(original.get(resource_name, []))
            resource_updated = set(updated.get(resource_name, []))
            new_orphans = resource_original - resource_updated
            new_adopted = resource_updated - resource_original

            if len(new_orphans) != 0 or len(new_adopted) != 0:
                child_domain = cls.children_resources[resource_name]
                # We remove our foreign key (with our ancestors) in the orphans' documents
                parent_accounts = py_(perms).pluck('account').uniq().value()
                cls.disinherit(_id, child_domain, new_orphans, parent_accounts)

                # We remove other parents (some groups may override it and do nothing here)
                # Inherit, executed after, will propagate this changes to the descendants
                cls.remove_other_parents_of_type(child_domain, new_adopted)

                # We add our foreign key (with our ancestors) in the new adopted's documents
                # and we propagate all changes to our descendants
                cls.inherit(_id, ancestors, child_domain, new_adopted, perms)

    @classmethod
    def disinherit(cls, parent_id: str, child_domain: Type[Domain], children: Iterable, parent_accounts: List[str]):
        """
        Removes the *ancestors* dict the children inherited from the parent, and then recursively updates
        the ancestors of the descendants of the children.

        :param parent_id: The id of the parent, used as FK.
        :param child_domain: The domain of the children. Note that this forces all children to be of the same @type.
        Call inherit as many times as types of children you have.
        :param children: A list of children ids.
        """
        q = {'$pull': {'ancestors': {'@type': cls.resource_settings._schema.type_name, '_id': parent_id}}}
        full_children = child_domain.update_raw_get(children, q)

        cls._remove_children_perms(full_children, parent_accounts, child_domain)

        # We disinherit any component the devices have (only devices have components)
        # todo materialize 'components' field into group
        components = compact(flatten(pluck(full_children, 'components')))
        if len(components) > 0:
            cls.disinherit(parent_id, ComponentDomain, components, parent_accounts)
        # Inherit children groups
        if issubclass(child_domain, GroupDomain):
            cls._update_inheritance_grandchildren(full_children, child_domain, accounts_to_remove=parent_accounts)

    @classmethod
    def remove_other_parents_of_type(cls, child_domain: Type[Domain], children: Iterable):
        """
        Removes any parent of the same type of the parent children have.

        By default a resource can only have one parent of a type, so we remove another parent of the same
        type that our children have. Some groups like lots of packages *share parenthood* (they allow
        multiple parents simultaniously for their children) and they override this method with a *pass*.

        This method does not recursively update descendants –use **inherit() after**.

        :param child_domain: The domain of the children. Note that this forces all children to be of the same @type.
        Call inherit as many times as types of children you have.
        :param children: A list of children ids.
        """
        query = {'$pull': {'ancestors': {'@type': cls.resource_settings._schema.type_name}}}
        child_domain.update_raw(children, query)

    @classmethod
    def inherit(cls, parent_id: str, parent_ancestors: list, child_domain: Type[Domain], children: Iterable,
                parent_perms: Perms = None, accounts_to_remove: List[str] = None):
        """
        Copies all the ancestors of the parent to the children (adding the parent as an ancestor), and then
        recursively updates the ancestors of the descendants of the children.

        Certain kind of groups behave differently here and they override this method.
        :param parent_id: The id of the parent, used as FK.
        :param parent_ancestors: An *ancestor dict*, see the Group Schema for more info.
        :param child_domain: The domain of the children. Note that this forces all children to be of the same @type.
        Call inherit as many times as types of children you have.
        :param children: A list of children id.
        """
        # Inheritance mechanism:
        # - If parent is place, inherit all its places.
        #  - ancestors.prepend({'@type': 'Place', 'name': '', 'places': [_id]})
        # - If parent is lot:
        #  - If child is lot, inherit places and lots
        #    - ancestors.prepend({'@type': 'Lot', 'name': '', 'places': [_id], 'lots': [_id]})
        #  - If child is package or device, inherit only lots
        #    - ancestors.prepend({'@type': 'Lot', 'name': '', 'lots': [_id]})
        # - If parent is package (then child can only be package or device) inherit everything:
        #    - ancestors.prepend({'@type': 'Lot', 'name': '', 'lots': [_id], 'packages': [_id], 'places': [_id]})

        # As places only have places is the same as inheriting everything they have.
        groups = cls.children_resources.keys()
        full_children = cls._inherit(groups, parent_id, parent_ancestors, child_domain, children, parent_perms,
                                     accounts_to_remove)
        if issubclass(child_domain, GroupDomain):
            cls._update_inheritance_grandchildren(full_children, child_domain, parent_perms, accounts_to_remove)

    @classmethod
    def _inherit(cls, groups_to_inherit: Iterable, parent_id: str, parent_ancestors: list, child_domain: Type[Domain],
                 children: Iterable, parent_perms: Perms = None, accounts_to_remove: List[str] = None) -> list:
        """
        Copies the passed-in ancestors to the children.

        Ancestors are merged in a set, avoiding repetition of ancestors for resources with multiple parents.

        When pasting the copy, it tries to identify an existing ancestors dictionary given by the parent,
        otherwise creates a new one.
        """
        # The child_ancestors for the 'new' db query
        child_ancestors_new = {'@type': cls.resource_settings._schema.type_name, '_id': parent_id}
        # The child_ancestors for the 'update' db query
        child_ancestors_update = {'$set': {}}
        for resource_name in groups_to_inherit:
            child_ancestors_new[resource_name] = set()  # We want to explicitly 'set' for the db
            for grandparent in parent_ancestors:
                if resource_name in grandparent:
                    child_ancestors_new[resource_name] |= set(grandparent[resource_name])
                if grandparent['@type'] == Naming.type(resource_name):  # We add the grandparent itself
                    child_ancestors_new[resource_name].add(grandparent['_id'])
            # Let's copy the result of the iteration to the update query
            child_ancestors_update['$set']['ancestors.$.' + resource_name] = child_ancestors_new[resource_name]

            # Permissions
            if parent_perms:
                child_ancestors_update['$set']['perms'] = parent_perms
        return cls._update_db(parent_id, children, child_ancestors_new, child_ancestors_update, child_domain,
                              parent_perms, accounts_to_remove)

    @classmethod
    def _update_db(cls, parent_id: str, children: Iterable, ancestors_new: dict, ancestors_update: dict,
                   child_domain: Type[Domain], parent_perms: Perms = None, parent_accounts_remove: List[str] = None):
        new_children = []
        for child in children:  # We cannot run all the children at once when catching exceptions
            try:
                # Let's try to update an existing ancestor dict (this is with the same _id and @type),
                # Note that this only will succeed when a relationship child-parent already exists, and this happens
                # when we are updating the grandchilden (and so on) after adding/deleting a relationship
                eq = {'ancestors.@type': ancestors_new['@type'], 'ancestors._id': parent_id}
                full_child, *_ = child_domain.update_raw_get(child, ancestors_update, extra_query=eq, upsert=True)
            except OperationFailure as e:
                if e.code == 16836:
                    # There is not an ancestor dict, so let's create one
                    # This only happens when creating a relationship parent-child
                    update_query = {
                        '$push': {'ancestors': {'$each': [ancestors_new], '$position': 0}},
                    }
                    if parent_perms is not None:
                        # We are inheriting new permissions
                        update_query['$set'] = {'perms': parent_perms}
                    full_child, *_ = child_domain.update_raw_get(child, update_query)
                else:
                    raise e
            if full_child is None:
                raise GroupNotFound('{} couldn\'t inheritance because it does not exist'.format(child))
            new_children.append(full_child)
            # todo materialize components
            components = full_child.get('components', [])  # Let's update the components
            cls._update_db(parent_id, components, ancestors_new, ancestors_update, ComponentDomain, parent_perms,
                           parent_accounts_remove)

        # Update perms for all children
        if parent_accounts_remove is not None:
            # We are inheriting the removal of permissions
            cls._remove_children_perms(new_children, parent_accounts_remove, child_domain)

        return new_children

    @classmethod
    def _update_inheritance_grandchildren(cls, full_children: list, child_domain: Type['GroupDomain'],
                                          parent_perms: Perms = None, accounts_to_remove: List[str] = None):
        """
        Moves forward in updating the inheritance for the descendants by calling inherit, passing the
        child as the parent and the grand-children as children.

        As *inherit* calls this method, recursively they update the ancestors of all descendants.
        :param full_children: The children whose children (our grand-children) will be updated
        :param child_domain: The domain of the children. Note that this forces all children to be the same @type.
        """
        if child_domain.resource_settings.resource_name() in Group.resource_names:
            for full_child in full_children:
                for name in child_domain.children_resources.keys():
                    grandchildren_domain = child_domain.children_resources[name]
                    grandchildren = set(full_child['children'][name]) if name in full_child['children'] else set()
                    if len(grandchildren) > 0:
                        child_domain.inherit(full_child['_id'], full_child['ancestors'], grandchildren_domain,
                                             grandchildren, parent_perms, accounts_to_remove)

    @classproperty
    def children_resources(cls) -> Dict[str, Type[Domain]]:
        """Dict containing the ResourceDomain of each type of children a group can have."""
        if not hasattr(cls, '_children_resources'):
            from ereuse_devicehub.resources.group.physical.place.domain import PlaceDomain
            from ereuse_devicehub.resources.group.physical.package.domain import PackageDomain
            from ereuse_devicehub.resources.group.physical.pallet.domain import PalletDomain
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
                PalletDomain.resource_settings.resource_name(): PalletDomain
            }
            types = {DeviceDomain.resource_settings.resource_name(), ComponentDomain.resource_settings.resource_name()}
            types |= cls.resource_settings._schema.resource_names
            cls._children_resources = pick(children_resources, *types)
        return cls._children_resources

    @classmethod
    def is_parent(cls, parent_type: str, parent_id: str, child_id: str) -> bool:
        q = {'_id': child_id, 'ancestors': {'$elemMatch': {'@type': parent_type, '_id': parent_id}}}
        try:
            return bool(cls.get_one(q))
        except ResourceNotFound:
            return False

    @classmethod
    def get_descendants(cls, child_domain: Type[Domain], parent_ids: str or list) -> list:
        """
        Get the descendants of this class type of the given ancestor.
        :param child_domain: The child domain.
        :param parent_ids: The id of a parent or a list of them. We retrieve descendants of **any** parent.
        """
        # The following is possible because during the inheritance, we only add to 'ancestors' the valid ones.
        type_name = cls.resource_settings._schema.type_name
        ids = parent_ids if type(parent_ids) is list else [parent_ids]
        query = {
            '$or': [
                {'ancestors': {'$elemMatch': {'@type': type_name, '_id': {'$in': ids}}}},
                {'ancestors': {'$elemMatch': {cls.resource_settings.resource_name(): {'$elemMatch': {'$in': ids}}}}}
            ]
        }
        return child_domain.get(query)

    @classmethod
    def get_all_descendants(cls, parent_ids: str or list) -> list:
        # Todo enhance by performing only one query
        return map_values(cls.children_resources, lambda domain: cls.get_descendants(domain, parent_ids))

    @classmethod
    def _remove_children_perms(cls, full_children, parent_accounts, child_domain):
        # Remove permissions
        for child in full_children:
            accounts_to_remove = difference(parent_accounts, child.get('sharedWith', []))
            comparator = lambda a, b: a['account'] == b
            perms = difference_with(child['perms'], accounts_to_remove, comparator=comparator)
            if len(perms) != len(child['perms']):
                child_domain.update_one_raw(child['_id'], {'$set': {'perms': perms}})
                child['perms'] = perms  # As we pass it into another function, just in case it is used later

    @classmethod
    def update_and_inherit_perms(cls, resource_id: dict, resource_type: str, label: str, shared_with: Set[ObjectId],
                                 old_perms: List[dict], new_perms: List[dict]):
        """
        Update the sharedWith of the resource and inherits the **changed** (and only the changed) permissions to its
        descendants.

        sharedWith is updated for both the resource and its descendants, if needed; this updates the account too.

        Be aware that the cost of this method greatly increases by the number of descendants.

        :raise UserHasExplicitDbPerms: You can't share to accounts that already have full access to this database.
        """
        if old_perms != new_perms:
            # Add new explicit shares to the *sharedWith* list and materialize it in the affected accounts
            accounts_to_add = set(pluck(new_perms, 'account')) - set(pluck(old_perms, 'account'))
            shared_with |= accounts_to_add
            # This can raise an exception and thus need to be executed before any modification in the DB
            AccountDomain.add_shared(accounts_to_add, resource_type, AccountDomain.requested_database, resource_id,
                                     label)

            # We compute which permissions we need to set (or re-set because they changed)
            accounts_to_remove = set(pluck(old_perms, 'account')) - set(pluck(new_perms, 'account'))
            shared_with = cls.remove_shared_with(resource_type, resource_id, shared_with, accounts_to_remove)

            # Inherit
            new_modified_perms = difference(new_perms, old_perms)  # New or modified permissions to write to descendants
            for resource_name, domain in cls.children_resources.items():
                for descendant in cls.get_descendants(domain, resource_id):
                    # Remove permissions
                    f = lambda a, b: a['account'] == b
                    perms = difference_with(descendant['perms'], list(accounts_to_remove), comparator=f)

                    # Set or re-set new or updated permissions
                    perms = union_by(new_modified_perms, perms, iteratee=lambda x: x['account'])

                    q = {'$set': {'perms': perms}}

                    # Remove accounts that lost permission from sharedWith
                    if resource_name != Device.resource_name:
                        descendant_shared_with = set(descendant.get('sharedWith', set()))
                        descendant_shared_with = cls.remove_shared_with(descendant['@type'], descendant['_id'],
                                                                        descendant_shared_with, accounts_to_remove)
                        q['$set']['sharedWith'] = descendant_shared_with

                    # Update the changes of the descendant in the database
                    domain.update_one_raw(descendant['_id'], q)
        return shared_with

    @classmethod
    def remove_shared_with(cls, type_name: str, _id: str or ObjectId, shared_with: Set[ObjectId],
                           accounts_to_remove: Set[ObjectId]) -> Set[ObjectId]:
        """Removes the shared accounts, updating the accounts database. Returns the new sharedWith."""
        db = AccountDomain.requested_database
        AccountDomain.remove_shared(db, shared_with.intersection(accounts_to_remove), _id, type_name)
        return set(shared_with) - accounts_to_remove


class GroupNotFound(ResourceNotFound):
    pass
