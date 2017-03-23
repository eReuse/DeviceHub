from eve.utils import document_etag
from flask import current_app as app

from ereuse_devicehub.exceptions import RequestAnother
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.device.settings import DeviceEvent
from ereuse_devicehub.rest import execute_delete
from ereuse_devicehub.utils import Naming


def generate_etag(resource: str, items: list):
    if resource in Device.resource_types:
        for item in items:
            item['_etag'] = document_etag(item,
                                          app.config['DOMAIN'][Naming.resource(item['@type'])]['etag_ignore_fields'])


def post_benchmark(resource: str, devices: list):
    """
    Sets the result of one benchmark into 'benchmarks' array.

    Use this method only in POST.
    :param resource:
    :param devices:
    """
    if resource in Device.resource_types:
        for device in devices:
            if 'benchmark' in device:
                device['benchmarks'] = [device['benchmark']]
                del device['benchmark']


def autoincrement(resource: str, devices: list):
    if resource in Device.resource_types:
        for device in devices:
            if '_id' not in device:
                # string makes this compatible with other systems that use custom id
                device['_id'] = str(get_next_sequence())


def get_next_sequence():
    return app.data.driver.db.device_sequence.find_and_modify(
        query={'_id': 1},
        update={'$inc': {'seq': 1}},
        new=True,
        upsert=True
    ).get('seq')


def materialize_public_in_components(resource: str, devices: list):
    """
    Materializes the 'public' field of the passed in devices in their components.
    :param resource:
    :param devices:
    :return:
    """
    if resource in Device.resource_types:
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


class MaterializeEvents:
    """
        Materializes some fields of the events in the affected device, benefiting searches. To keep minimum space,
        only selected fields are materialized (which you can check in the following tuple)
    """
    fields = {
        '_id', '@type', 'label', 'date', 'incidence', 'secured', 'comment', 'success', 'error', 'type', 'receiver',
        'receiverOrganization', 'to', 'toOrganization', 'secured', 'byUser', 'geo', '_updated'
    }

    @classmethod
    def materialize_events(cls, resource: str, events: list):
        if resource in DeviceEvent.resource_types:
            for event in events:
                trimmed_event = {field_name: event[field_name] for field_name in cls.fields if field_name in event}
                query = {'$push': {'events': {'$each': [trimmed_event], '$position': 0}}}
                devices = [event['device']] if 'device' in event else event['devices']
                if 'parent' in event:  # Let's materialize the events (test, erasure...) of the component to the parent
                    devices.append(event['parent'])
                DeviceDomain.update_raw(devices, query)
                DeviceDomain.update_raw(event.get('components', []), query)

    @classmethod
    def dematerialize_event(cls, resource: str, event: dict):
        if event.get('@type') in DeviceEvent.types:
            device = [event['device']] if 'device' in event else []
            parent = [event['parent']] if 'parent' in device else []
            for device_id in event.get('devices', []) + event.get('components', []) + device + parent:
                DeviceDomain.update_raw(device_id, {'$pull': {'events': {'_id': event['_id']}}})


def redirect_to_first_snapshot(resource, request, lookup):
    """
    DELETE /device should be an internal method, but it is open to redirect to the door that is going to effictevely
    delete the device; this is the first Snapshot that made the Register that made the device.
    """
    if resource in Device.resource_types:
        snapshot_id = str(DeviceEventDomain.get_first_snapshot(lookup['_id'])['_id'])
        execute_delete(Naming.resource('devices:Snapshot'), snapshot_id)
        raise RequestAnother('', 204)
