from eve.utils import document_etag
from ereuse_devicehub.app import app
from ereuse_devicehub.resources.device.device import Device
from ereuse_devicehub.utils import Naming


def generate_etag(resource: str, items: list):
    if resource in Device.resource_types():
        for item in items:
            item['_etag'] = document_etag(item,
                                          app.config['DOMAIN'][Naming.resource(item['@type'])]['etag_ignore_fields'])


def get_icon(resource: str, item: dict):
    if item['@type'] in Device.get_types():
        type = item['type'] if 'type' in item else item['@type']
        item['icon'] = 'devices/icons/' + type + '.svg'


def get_icon_resource(resource: str, response: dict):
    for item in response['_items']:
        get_icon(resource, item)


def post_benchmark(resource: str, devices: list):
    """
    Sets the result of one benchmark into 'benchmarks' array.

    Use this method only in POST.
    :param resource:
    :param devices:
    """
    if resource in Device.resource_types():
        for device in devices:
            if 'benchmark' in device:
                device['benchmarks'] = [device['benchmark']]
                del device['benchmark']


def autoincrement(resource: str, devices: list):
    if resource in Device.resource_types():
        for device in devices:
            device['_id'] = str(get_next_sequence())  # string makes this compatible with other systems that use custom id


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
    if resource in Device.resource_types():
        for device in devices:
            if 'components' in device:
                Device.update(device['components'], {'$set': {'public': device.get('public', False)}})


def materialize_public_in_components_update(resource: str, device: dict, original: dict):
    """
    The same as :func materialize_public_in_components: but thought to be used with PATCH methods.
    :param resource:
    :param device:
    :param original:
    """
    # PATCH doesn't need to include components if we are not changing them
    # We have already saved the device to the DB so we can securely modify the device dictionary
    if original['@type'] in Device.get_types():
        if 'components' not in device:
            device['components'] = original['components']
        materialize_public_in_components(Naming.resource(original['@type']), [device])

