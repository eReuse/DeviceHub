from eve.utils import document_etag

from app.app import app
from app.device.device import Device
from app.utils import get_resource_name


def generate_etag(resource: str, items: list):
    if resource in Device.resource_types():
        for item in items:
            item['_etag'] = document_etag(item,
                                          app.config['DOMAIN'][get_resource_name(item['@type'])]['etag_ignore_fields'])


def get_icon(resource: str, item: dict):
    if item['@type'] in Device.get_types():
        type = item['type'] if 'type' in item else item['@type']
        item['icon'] = 'devices/icons/' + type + '.svg'


def get_icon_resource(resource: str, response: dict):
    for item in response['_items']:
        get_icon(resource, item)


def autoincrement(resource: str, devices: list):
    if resource in Device.resource_types():
        for device in devices:
            device['_id'] = str(get_next_sequence())  # todo find a way to use integer


def get_next_sequence():
    return app.data.driver.db.device_sequence.find_and_modify(
        query={'_id': 1},
        update={'$inc': {'seq': 1}},
        new=True,
        upsert=True
    ).get('seq')