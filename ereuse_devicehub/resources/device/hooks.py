from bson import ObjectId
from eve.utils import document_etag
from flask import current_app
from pydash import find
from pymongo import ReturnDocument

from ereuse_devicehub.exceptions import RequestAnother, StandardError
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.device.migrate.settings import Migrate
from ereuse_devicehub.resources.event.domain import EventNotFound
from ereuse_devicehub.rest import execute_delete
from ereuse_devicehub.utils import Naming


def generate_etag(resource: str, items: list):
    if resource in Device.resource_names:
        for item in items:
            ignore_fields = current_app.config['DOMAIN'][Naming.resource(item['@type'])]['etag_ignore_fields']
            item['_etag'] = document_etag(item, ignore_fields)


def post_benchmark(resource: str, devices: list):
    """
    Sets the result of one benchmark into 'benchmarks' array.

    Use this method only in POST.
    :param resource:
    :param devices:
    """
    if resource in Device.resource_names:
        for device in devices:
            if 'benchmark' in device:
                device['benchmarks'] = [device['benchmark']]
                del device['benchmark']


def autoincrement(resource: str, devices: list):
    if resource in Device.resource_names:
        for device in devices:
            if '_id' not in device:
                # string makes this compatible with other systems that use custom id
                device['_id'] = str(get_next_sequence())


def get_next_sequence() -> int:
    """Autoincrements the _id."""
    # We force using the same database as the ones where devices are. This is needed as, unlike resources in their
    # settings, we do not tell to python-eve at any moment where is this collection stored at.
    # Note that if we do not put this, eve tries to guess scanning the URL for a resource name; this works
    # if we are doing POST /register (register is in the same db) but not POST /account (different db)
    return current_app.data.pymongo(Device.resource_name).db.device_sequence.find_one_and_update(
        filter={'_id': 1}, update={'$inc': {'seq': 1}}, return_document=ReturnDocument.AFTER, upsert=True
    ).get('seq')


def materialize_public_in_components(resource: str, devices: list):
    """
    Materializes the 'public' field of the passed in devices in their components.
    :param resource:
    :param devices:
    :return:
    """
    if resource in Device.resource_names:
        for device in devices:
            if device.get('components'):  # If empty do not try to execute
                DeviceDomain.update_raw(device['components'], {'$set': {'public': device.get('public', False)}})


def materialize_public_in_components_update(resource: str, device: dict, original: dict):
    """
    The same as :func materialize_public_in_components: but thought to be used with PATCH methods.
    :param resource:
    :param device:
    :param original:
    """
    # PATCH doesn't need to include components if we are not changing them
    # We have already saved the device to the DB so we can securely modify the device dictionary
    if original['@type'] in Device.types:
        if 'components' not in device:
            device['components'] = original['components']
        materialize_public_in_components(Naming.resource(original['@type']), [device])


def avoid_deleting_if_device_has_migrate(resource_name: str, device: dict):
    """Deleting a device that has a Migrate would mean to undo the migrate, something we are not ready to do."""
    if resource_name in Device.resource_names:
        event = find(device['events'], {'@type': Migrate.type_name})
        if event:
            raise DeviceHasMigrate(event['_id'], device['_id'])


def redirect_to_first_snapshot_or_register(resource, _, lookup):
    """
    DELETE /device should be an internal method, but it is open to redirect to the door that is going to effectively
    delete the device; this is, or the first Snapshot that made the Register that made the device, or directly
    such Register, if the device was not created through a Snapshot.
    """

    # todo can we just always go to the first Register regardless the device was created with a Snapshot or not?
    def _redirect_to_first_event(event_resource_name: str):
        event_id = str(DeviceEventDomain.get_first_event(event_resource_name, lookup['_id'])['_id'])
        execute_delete(Naming.resource(event_resource_name), event_id)

    if resource in Device.resource_names:
        try:
            _redirect_to_first_event('devices:Snapshot')
        except EventNotFound:
            _redirect_to_first_event('devices:Register')
        raise RequestAnother('', 204)


class DeviceHasMigrate(StandardError):
    status_code = 405  # Method not allowed

    def __init__(self, event_id: ObjectId, device_id: str):
        message = 'You can\'t delete a device that has a Migrate event.'.format(event_id, device_id)
        super().__init__(message)
