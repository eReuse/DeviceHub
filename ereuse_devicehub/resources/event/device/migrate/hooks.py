from contextlib import suppress

import pymongo
from flask import Response
from flask import current_app
from flask import g
from flask import json

from ereuse_devicehub.exceptions import SchemaError, InnerRequestError
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.device.component.settings import Component
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.device.migrate.migrate import DeviceHasMigrated, MigrateSubmitter, \
    MigrateTranslator
from ereuse_devicehub.resources.event.device.migrate.migrate_creator import MigrateCreator
from ereuse_devicehub.resources.event.device.migrate.settings import Migrate
from ereuse_devicehub.resources.event.domain import EventNotFound
from ereuse_devicehub.resources.group.physical.place.domain import PlaceDomain
from ereuse_devicehub.resources.group.physical.place.settings import Place
from ereuse_devicehub.rest import execute_delete, execute_patch
from ereuse_devicehub.security.request_auth import AgentAuth
from ereuse_devicehub.utils import Naming

MIGRATE_RETURNED_SAME_AS = 'migrate_returned_same_as'


def submit_migrate(migrates: dict):
    """
    Sends a Migrate event to the other DeviceHub.
    Note as the other DeviceHub requires the url of this event,
    this method needs to be executed after reaching the Database.
    """
    for migrate in migrates:
        if 'to' in migrate:
            auth = AgentAuth(migrate['to']['baseUrl'])
            submitter = MigrateSubmitter(current_app, MigrateTranslator(current_app.config), auth=auth)
            try:
                response, *_ = submitter.submit(migrate, AccountDomain.get_requested_database())
                migrate['to']['url'] = migrate['to']['baseUrl'] + response['_links']['self']['href']
                _update_same_as(response['returnedSameAs'])
            except InnerRequestError as e:
                execute_delete(Migrate.resource_name, migrate['_id'])
                raise e
            else:
                update = {'$set': {'to.url': migrate['to']['url'], 'devices': [_id for _id in migrate['devices']]}}
                DeviceEventDomain.update_one_raw(migrate['_id'], update)


def _update_same_as(returned_same_as: dict):
    for url, same_as in returned_same_as.items():
        _id = url.split('/')[-1]
        device = DeviceDomain.get_one({'_id': _id})
        same_as = set(device.get('sameAs', [])) | set(same_as)
        DeviceDomain.update_one_raw(_id, {'$set': {'sameAs': list(same_as)}})


def create_migrate(migrates: list):
    """
    Manages the creation of a Migrate event, like doing so for the devices.
    Heavily inspired by the hook 'on_insert_snapshot', uses the same idea on a group of devices.
    """
    all_events = []  # We will delete all events if exception
    try:
        for migrate in migrates:
            if 'from' in migrate:
                setattr(g, MIGRATE_RETURNED_SAME_AS, dict())
                devices_id = []
                migrate['components'] = []
                for device in migrate['devices']:
                    if device['@type'] in Component.types:
                        raise SchemaError('devices', 'You cannot directly migrate components.')
                    creator = MigrateCreator(device, device.pop('components'))
                    events = creator.execute()
                    all_events += events
                    migrate['events'] = [new_events['_id'] for new_events in events]
                    devices_id.append(device['_id'])
                    migrate['components'] += [component['_id'] for component in creator.components]
                    migrate['unsecured'] = creator.unsecured
                    getattr(g, MIGRATE_RETURNED_SAME_AS).update(creator.returned_same_as)
                from ereuse_devicehub.resources.hooks import set_date
                set_date(None, migrates)
                migrate['devices'] = devices_id
    except Exception as e:
        for event in all_events:
            # Could result in 404 (ex: delete an 'Add' after deleting 'Register' of the same device)
            execute_delete(Naming.resource(event['@type']), event['_id'])
        raise e


def return_same_as(_, payload: Response):
    """
    Sets JSON Header link referring to @type
    """
    if (payload._status_code == 201) and hasattr(g, MIGRATE_RETURNED_SAME_AS):
        data = json.loads(payload.data.decode(payload.charset))
        data['returnedSameAs'] = getattr(g, MIGRATE_RETURNED_SAME_AS)
        delattr(g, MIGRATE_RETURNED_SAME_AS)
        payload.data = json.dumps(data)


def check_migrate_insert(_, resources: list):
    for migrate in resources:
        check_migrate(_, migrate)


def check_migrate_update(_, resource: dict, __):
    check_migrate(_, resource)


def check_migrate(_, resource: dict):
    """
    Raises an exception if any of the device(s) in the resource is in another database, as a result of a Migrate event.

    This is done to avoid adding/modifying/deleting events or places that have a relationship with a device that
    is not legally bound in a DeviceHub.

    The method checks if the last Migrate has a 'to' field, meaning the device is in another database and has not
    come back.
    :raises DeviceHasMigrated
    """
    devices = ([resource['device']] if 'device' in resource else [])
    devices += resource.get('children', {}).get('devices', []) + resource.get('devices', [])
    for device_id in devices:
        with suppress(EventNotFound):
            # todo can it be done with only one access to the DB for all devices (optimization)?
            # Note that this is executed for every post / delete /update / patch, resulting in queries = n of devices
            query = {'@type': Migrate.type_name, 'devices': {'$in': [device_id]}}
            last_migrate = DeviceEventDomain.get_one({'$query': query, '$orderby': {'_created': pymongo.DESCENDING}})
            if 'to' in last_migrate:
                raise DeviceHasMigrated(device_id, last_migrate)


def remove_devices_from_place(migrates: dict):
    """
    Removes the devices that have been moved to another db from all places, as accounts are not supposed to interact
    with them anymore, and they would end up stuck in those places.
    """
    for migrate in migrates:
        if 'to' in migrate:
            devices_to_remove = set(migrate['devices'])
            for place in PlaceDomain.get({'children.devices': {'$in': migrate['devices']}}):
                payload = {
                    '@type': Place.type_name,
                    'children': {'devices': list(set(place['children'].get('devices', [])) - devices_to_remove)}
                }
                execute_patch(Place.resource_name, payload, place['_id'])
