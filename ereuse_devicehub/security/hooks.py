from contextlib import suppress
from typing import List

from bson import ObjectId
from flask import current_app, Request, json
from pydash import find, pluck, difference

from ereuse_devicehub.exceptions import InsufficientDatabasePerm
from ereuse_devicehub.resources.account.domain import AccountDomain, NotADatabase
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.exceptions import DeviceNotFound
from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.device.reserve.settings import Reserve
from ereuse_devicehub.resources.event.settings import Event
from ereuse_devicehub.resources.group.settings import Group
from ereuse_devicehub.security.perms import READ, RESOURCE_PERMS


def check_get_perms_for_list_of_items(resource_name: str, request: Request, lookup: dict):
    """Ensure user has sufficient permission to GET the resources."""
    HAS_PERM = {'$elemMatch': {'account': AccountDomain.actual['_id'], 'perm': READ}}
    # Are we querying a list of resources? (eg: www.ex.com/foo?where={})
    if type(lookup.get('_id', None)) not in {ObjectId, int, str}:
        # has_full_db_access will throw notADatabase for endpoints that
        # do not use specific databases, but we don't care for those
        with suppress(NotADatabase):
            if not current_app.auth.has_full_db_access():
                if resource_name in Event.resource_names:
                    # events don't have a 'perms' property
                    # and they can be accessed if one of its devices can be accessed
                    # Note that resource_name is usually 'events' in this case, not the
                    # specific resource type of event
                    try:
                        where = json.loads(request.args['where'])
                        DeviceDomain.get_one({'_id': where['dh$eventOfDevice'], 'perms': HAS_PERM})
                    except (KeyError, DeviceNotFound):
                        raise InsufficientDatabasePerm(resource_name, ids=[''])
                else:
                    # Only get resources that the user has READ access to
                    lookup['perms'] = HAS_PERM


def check_get_perms_for_item(resource_name: str, resource: dict):
    """
    Ensure user has sufficient permission to GET a **specific** resource.

    For now this means accessing:
    - a device or a group which for you have access to.
    - An event that has one device that is accessible to

    This avoids you accessing any other resource, like accounts.
    """
    if '_items' not in resource:  # Are we querying a resource (eg: www.ex.com/foo/bar)
        with suppress(NotADatabase):
            if not current_app.auth.has_full_db_access():
                read_perm = lambda p: p == {'account': AccountDomain.actual['_id'], 'perm': READ}
                if resource_name in Device.resource_names | Group.resource_names:
                    if not find(resource.get('perms', []), read_perm):
                        raise InsufficientDatabasePerm(resource_name, ids=[resource['_id']])
                elif resource_name in Event.resource_names:
                    # Note that resource_name is usually 'events' in this case, not the
                    # specific resource type of event
                    try:
                        q = {
                            '_id': {
                                '$in': DeviceEventDomain.devices_id(resource, DeviceEventDomain.DEVICES_ID_COMPONENTS)
                            },
                            'perms': {
                                '$elemMatch': {'account': AccountDomain.actual['_id'], 'perm': {'$in': RESOURCE_PERMS}}
                            }
                        }
                        DeviceDomain.get_one(q)
                    except DeviceNotFound:
                        raise InsufficientDatabasePerm(resource_name, ids=[resource['_id']])
                else:
                    raise InsufficientDatabasePerm(resource_name, ids=[resource['_id']])


def check_post_perms(resource_name: str, resources: List[dict]):
    """
    Ensure user has sufficient permission to POST.

    For now, this only checks that, if the user has no full db access, it is posting a Reserve event where
    it has READ permission on all devices.
    """
    with suppress(NotADatabase):
        if not current_app.auth.has_full_db_access():
            db = AccountDomain.requested_database
            if resource_name == Reserve.resource_name:
                for resource in resources:
                    # We don't need to check for access in group if we already check on all devices
                    # because you can't perform an event to empty group
                    q = {
                        '_id': {'$in': resource['devices']},
                        'perms': {
                            '$elemMatch': {'account': AccountDomain.actual['_id'], 'perm': {'$in': RESOURCE_PERMS}}
                        }
                    }
                    accessible_devices = DeviceDomain.get(q)
                    non_accessible_devices = difference(resource['devices'], pluck(accessible_devices, '_id'))
                    if non_accessible_devices:
                        ids = pluck(non_accessible_devices, '_id')
                        raise InsufficientDatabasePerm(DeviceDomain.resource_name, db=db, ids=ids)
            else:
                raise InsufficientDatabasePerm(resource_name, db=db)
