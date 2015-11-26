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
        item['icon'] = '//devices/icons/' + type + '.svg'


def get_icon_resource(resource: str, response: dict):
    for item in response['_items']:
        get_icon(resource, item)
