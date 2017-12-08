from collections import Iterable
from typing import Dict, List, Set, Type

from bson import ObjectId
from passlib.utils import classproperty
from pydash import compact, difference, difference_with, flatten, map_values, pick, pluck, py_, union_by
from pymongo.errors import OperationFailure

from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.device.component.domain import ComponentDomain
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.domain import Domain, ResourceNotFound
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.group.settings import Group, GroupSettings
from ereuse_utils.naming import Naming

Perms = List[Dict[str, str]]


# noinspection PyProtectedMember
class GroupDomain(Domain):
    """
    Manages group-device-event inheritance with permissions.

    - Use ``update_children()`` to create
    """
    resource_settings = GroupSettings

    @classmethod
    def update_children(cls, original: dict, updated: dict, ancestors: list, _id: str or None, perms: Perms):
        """
        Updates the children of a group to reflect what says in the ``original`` field, materializing and affecting
        other resources and their permissions.

        :param original: The original *children* field.
        :param updated: The new *children* field.
        :param ancestors: The *ancestors* field.
        :param _id: The id of the group.
        :param perms: The *perms* field.
        """
        # todo there is no control (only in client) to prevent "shared parenting"
        # todo (resources can only have 1 parent, except when their parent is lots
        # groups other than lots
        # todo to "share" children (one children - multiple lots)
        for resource_name in cls.children_resources.keys():
            resource_original = set(original.get(resource_name, []))
            resource_updated = set(updated.get(resource_name, []))
            new_orphans = resource_original - resource_updated
            new_adopted = resource_updated - resource_original

            if new_orphans or new_adopted:
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
    def disinherit(cls, parent_id: str, child_domain: Type[Domain], children: Set[str], parent_accounts: List[str]):
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

        cls._remove_perms(full_children, parent_accounts, child_domain)

        # We disinherit any component the devices have (only devices have components)
        components = compact(flatten(pluck(full_children, 'components')))
        if components:
            cls.disinherit(parent_id, ComponentDomain, set(components), parent_accounts)
        # Inherit children groups
        if issubclass(child_domain, GroupDomain):
            cls._update_inheritance_grandchildren(full_children, child_domain, accounts_to_remove=parent_accounts)

    @classmethod
    def remove_other_parents_of_type(cls, child_domain: Type[Domain], children: Set[str]):
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
    def inherit(cls, parent_id: str, parent_ancestors: list, child_domain: Type[Domain], children: Set[str],
                parent_perms: Perms = None, accounts_to_remove: List[str] = None):
        """
        Copies all the ancestors of the parent to the children (adding the parent as an ancestor), adding the
        *parents_perms* to the children xor removing accounts. Then, recursively it calls itself to update the
        descendants of the children.

        Note that inherit is called too when **dis**inheriting, because this method will transmit the result of
        the "disinheritance" to the descendants. This is why this method supports *accounts_to_remove* property.

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
                 resources: Set[str], parent_perms: Perms = None, accounts_to_remove: List[str] = None) -> list:
        """
        Copies the passed-in ancestors to the resources with the new permissions xor accounts to remove.

        This method specifically computes the *ancestors* property for each children and then calls to _update_db
        to update their value.

        Ancestors are merged in a set, avoiding repetition of ancestors for resources with multiple parents. When
        pasting the copy, it tries to identify an existing ancestors dictionary given by the parent,
        otherwise creates a new one.
        """
        # update_db needs 2 queries:
        # ancestors is a query that will be used when creating a relationship resource - parent
        # (the resource has a new parent)
        ancestors = {'@type': cls.resource_settings._schema.type_name, '_id': parent_id}
        # update_query is used to replace the ancestors of my parent
        update_query = {'$set': {}}
        for resource_name in groups_to_inherit:
            ancestors[resource_name] = set()  # We want to explicitly 'set' for the db
            # for all the parents of my parent
            for grandparent in parent_ancestors:
                if resource_name in grandparent:
                    ancestors[resource_name] |= set(grandparent[resource_name])
                if grandparent['@type'] == Naming.type(resource_name):  # We add the grandparent itself
                    ancestors[resource_name].add(grandparent['_id'])
            # Let's copy the result of the iteration to the update query
            update_query['$set']['ancestors.$.' + resource_name] = ancestors[resource_name]

        # ADDING PERMISSIONS
        # ------------------
        # Note that adding permissions is an easy query so we can do it here,
        # removing permissions is more difficult and is done inside _remove_perms(), executed inside of
        # _update_db
        if parent_perms:
            # inherit is executed after an ancestor moved to another one
            # in this case we override the perms of the descendants
            # todo if inherit is produced because a resource was **added** (not moved) to another lot
            # todo we are loosing the perms of the first lot, this should only be happening when moving
            # todo and not copying
            update_query['$set']['perms'] = parent_perms
        return cls._update_db(parent_id, resources, ancestors, update_query, child_domain,
                              parent_perms, accounts_to_remove)

    @classmethod
    def _update_db(cls, parent_id: str, resources: Set[str], ancestors_new: dict, update_query: dict,
                   child_domain: Type[Domain], parent_perms: Perms = None,
                   parent_accounts_remove: List[str] = None) -> List[dict]:
        """
        Executes in database for the passed-in resources and, for devices, their components too:

        - The query (the passed-in *ancestors_update*) computed in *_inherit*. This query
          updates *ancestors* and **adds** permissions.
        - Removes permissions when passing in *parent_acounts_remove* (internally calling *_remove_perms*)
        - For devices, adds and removes permissions for accounts when necessary (internally calling *_remove_perms*)
        """
        new_children = []
        for resource in resources:  # We cannot run all the resources at once when catching exceptions
            try:
                # Let's try to update an existing ancestor dict (this is with the same _id and @type),
                # Note that this only will succeed when a relationship child-parent already exists, and this happens
                # when we are updating the grandchilden (and so on) after adding/deleting a relationship
                eq = {'ancestors.@type': ancestors_new['@type'], 'ancestors._id': parent_id}
                full_child, *_ = child_domain.update_raw_get(resource, update_query, extra_query=eq, upsert=True)
            except OperationFailure as e:
                if e.code == 16836:
                    # There is not an ancestor dict, so let's create one
                    # This only happens when creating a relationship parent-child
                    new_query = {
                        '$push': {'ancestors': {'$each': [ancestors_new], '$position': 0}},
                    }
                    if parent_perms is not None:
                        # ADDING PERMISSIONS (bis)
                        # ------------------------
                        new_query['$set'] = {'perms': parent_perms}
                    full_child, *_ = child_domain.update_raw_get(resource, new_query)
                else:
                    raise e
            new_children.append(full_child)

            # UPDATE COMPONENTS
            # -----------------
            # Components of devices inherit exactly the same way as their parents, so
            # let's re-call this method with the components
            components = full_child.get('components', [])  # Let's update the components
            if components:
                cls._update_db(parent_id, components, ancestors_new, update_query, ComponentDomain, parent_perms,
                               parent_accounts_remove)

        # REMOVING PERMISSIONS
        # --------------------
        # Update perms for all children
        # Note that we took profit of the update above to add permissions
        if parent_accounts_remove:
            # We are inheriting the removal of permissions
            cls._remove_perms(new_children, parent_accounts_remove, child_domain)

        # ADDING PERMISSIONS TO EVENTS
        # ----------------------------
        if parent_perms:
            events_id = py_(new_children).pluck('events').flatten().pluck('_id').value()
            cls.add_perms_to_events(events_id, parent_perms)

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
                    if grandchildren:
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
    def _remove_perms(cls, resources: List[dict], accounts: List[str], child_domain: Type[Domain]):
        """
        Remove the permissions of the passed-in accounts from the resources.

        We drop the perm for those accounts that don't have explicit access.

        :param resources: Resources to remove permissions from.
        :param accounts: The accounts to remove, if don't have explicit access.
        :param child_domain: The child domain.
        """
        # Remove permissions
        for resource in resources:
            # Compute which accounts we remove
            accounts_to_remove = difference(accounts, resource.get('sharedWith', []))
            # Get the perms referencing those accounts
            perms = difference_with(resource['perms'], accounts_to_remove, comparator=lambda a, b: a['account'] == b)
            if len(perms) != len(resource['perms']):
                # We have lost some permissions
                child_domain.update_one_raw(resource['_id'], {'$set': {'perms': perms}})
                resource['perms'] = perms  # As we pass it into another function, just in case it is used later
                if resource['@type'] in Device.types:
                    # For devices, we need to update their events too
                    cls._remove_perms_in_event(accounts_to_remove, resource['_id'])

    @classmethod
    def _remove_perms_in_event(cls, accounts_to_remove_from_device: List[ObjectId], device_id: str):
        """
        Removes the permissions for the passed-in accounts, which the device is loosing, from the events.

        The accounts loose their permission only if, apart from the passed-in device (where the accounts are lost),
        the accounts don't have permissions on the other devices.

        :param accounts_to_remove_from_device: The accounts that we want to remove.
        :param device_id: The device that is dropping access for the accounts.
        :param events_id: The affected events.
        """
        from ereuse_devicehub.resources.event.device import DeviceEventDomain
        for event in DeviceEventDomain.get_devices_components_id([device_id]):
            # Which accounts have access to any of the other devices?
            # Those accounts with access will be saved, as it means the user can access the event because this
            # event represents a device that the account can access to.
            # Accounts that don't have access to other devices mean that they only had access to the
            # device we are removing, so we will drop access to the account as well.
            devices_id = DeviceEventDomain.devices_id(event, DeviceEventDomain.DEVICES_ID_COMPONENTS)
            devices_id.remove(device_id)
            devices = DeviceDomain.get_in('_id', devices_id)
            accounts_to_remove_from_event = difference(accounts_to_remove_from_device,
                                                       py_(devices).pluck('perms').flatten().pluck('account').value())
            if accounts_to_remove_from_event:
                cls._remove_perms([event], accounts_to_remove_from_event, DeviceEventDomain)

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

                    if resource_name not in Device.resource_names:
                        # Remove accounts that lost permission from sharedWith
                        descendant_shared_with = set(descendant.get('sharedWith', set()))
                        descendant_shared_with = cls.remove_shared_with(descendant['@type'], descendant['_id'],
                                                                        descendant_shared_with, accounts_to_remove)
                        q['$set']['sharedWith'] = descendant_shared_with
                    else:
                        # For devices, remove the perms from the events
                        cls._remove_perms_in_event(list(accounts_to_remove), descendant['_id'])
                        # add new perms to events
                        events_id = pluck(descendant['events'], '_id')
                        cls.add_perms_to_events(events_id, perms)

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

    @staticmethod
    def add_perms_to_events(events_id: List[str], perms: List[dict]):
        """Adds the perms to the events."""
        for event in DeviceEventDomain.get_in('_id', events_id):
            _perms = union_by(event['perms'], perms, iteratee=lambda x: x['account'])
            DeviceEventDomain.update_one_raw(event['_id'], {'$set': {'perms': _perms}})


class GroupNotFound(ResourceNotFound):
    pass
