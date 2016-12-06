import pymongo
from ereuse_devicehub.exceptions import SchemaError, InnerRequestError
from ereuse_devicehub.resources.device.component.settings import Component
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.device.migrate.migrate import DeviceHasMigrated, MigrateSubmit
from ereuse_devicehub.resources.event.device.migrate.migrate_creator import MigrateCreator
from ereuse_devicehub.resources.event.device.migrate.settings import Migrate
from ereuse_devicehub.resources.event.domain import EventNotFound
from ereuse_devicehub.resources.place.domain import PlaceDomain
from ereuse_devicehub.resources.place.settings import Place
from ereuse_devicehub.rest import execute_delete, execute_patch
from ereuse_devicehub.utils import Naming


def submit_migrate(migrates: dict):
    """
    Sends a Migrate event to the other DeviceHub.
    Note as the other DeviceHub requires the url of this event,
    this method needs to be executed after reaching the Database.
    """
    for migrate in migrates:
        if 'to' in migrate:
            submitter = MigrateSubmit(migrate['to'], migrate['devices'], migrate['_links']['self']['href'],
                                      migrate.get('label'), migrate.get('comment'))
            try:
                migrate['to']['url'] = submitter.execute()
            except InnerRequestError as e:
                execute_delete(Migrate.resource_name, migrate['_id'])
                raise e
            else:
                update = {'$set': {'to.url': migrate['to']['url'], 'devices': [_id for _id in migrate['devices']]}}
                DeviceEventDomain.update_one_raw(migrate['_id'], update)


def create_migrate(migrates: dict):
    """
    Manages the creation of a Migrate event, like doing so for the devices.
    Heavily inspired by the hook 'on_insert_snapshot', uses the same idea on a group of devices.
    """
    all_events = []  # We will delete all events if exception
    try:
        for migrate in migrates:
            if 'from' in migrate:
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
                from ereuse_devicehub.resources.hooks import set_date
                set_date(None, migrates)
                migrate['devices'] = devices_id
    except Exception as e:
        for event in all_events:
            # Could result in 404 (ex: delete an 'Add' after deleting 'Register' of the same device)
            execute_delete(Naming.resource(event['@type']), event['_id'])
        raise e


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
    devices = ([resource['device']] if 'device' in resource else []) + resource.get('devices', [])
    for device_id in devices:
        try:
            # todo can it be done with only one access to the DB for all devices (optimization)?
            # Note that this is executed for every post / delete /update / patch, resulting in queries = n of devices
            query = {'@type': Migrate.type_name, 'devices': {'$in': [device_id]}}
            last_migrate = DeviceEventDomain.get_one({'$query': query, '$orderby': {'_created': pymongo.DESCENDING}})
            if 'to' in last_migrate:
                raise DeviceHasMigrated(device_id, last_migrate)
        except EventNotFound:
            pass


def remove_devices_from_place(migrates: dict):
    """
    Removes the devices that have been moved to another db from all places, as accounts are not supposed to interact
    with them anymore, and they would end up stuck in those places.
    """
    for migrate in migrates:
        if 'to' in migrate:
            devices_to_remove = set(migrate['devices'])
            for place in PlaceDomain.get({'devices': {'$in': migrate['devices']}}):
                payload = {
                    '@type': Place.type_name,
                    'devices': list(set(place['devices']) - devices_to_remove)
                }
                execute_patch(Place.resource_name, payload, place['_id'])
