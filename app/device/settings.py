import copy
import pymongo

from app.account.user import Role
from app.utils import register_sub_types
from app.schema import thing
from app.validation import ALLOWED_WRITE_ROLES, HID_REGEX

product = dict(thing, **{
    'model': {
        'type': 'string'
    },
    'weight': {
        'type': 'float',  # In kilograms
    },
    'width': {
        'type': 'float'  # In meters
    },
    'height': {
        'type': 'float'  # In meters
    },
    'manufacturer': {
        'type': 'string',
    },
    'productId': {
        'type': 'string'
    },
})

individualProduct = dict(product, **{
    'serialNumber': {
        'type': 'string'
    }
})

device = copy.deepcopy(individualProduct)
device.update({
    '_id': {
        'type': 'string',
        'unique': True,
        ALLOWED_WRITE_ROLES: Role.SUPERUSER  # For recovery purposes
    },
    'icon': {
        'type': 'string',
        'readonly': True
    },
    'hid': {
        'type': 'hid'
    },
    'pid': {
        'type': 'string',
        'unique': True
    },
    'isUidSecured': {
        'type': 'boolean',
        'default': True
    },
    'labelId': {
        'type': 'string',  # Materialized label of the last snapshot
    },
    'components': {
        'type': 'list',
        'schema': {
            'type': 'string',
            'data_relation': {
                'resource': 'devices',
                'embeddable': True,
                'field': '_id'
            }
        },
        'default': []
    }
})

device_settings = {
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET'],
    'schema': device,
    'additional_lookup': {
        'field': 'hid',
        'url': 'regex("' + HID_REGEX + '")'
    },
    'item_url': 'regex("[\w]+")',
    'embedded_fields': ['components', 'tests'],
    'url': 'devices',
    'mongo_indexes': {
        '@type': [('@type', pymongo.DESCENDING)],
        '@type and subtype': [('@type', pymongo.DESCENDING), ('type', pymongo.DESCENDING)],
        '@type and _created': [('@type', pymongo.DESCENDING), ('_created', pymongo.DESCENDING)]
    },
    'etag_ignore_fields': ['hid', '_id', 'components', 'isUidSecured', '_created', '_updated', '_etag', 'speed',
                           'busClock', 'labelId']
}

device_sub_settings = {
    'resource_methods': ['POST'],
    'item_methods': ['DELETE'],
    'url': device_settings['url'] + '/',
    'datasource': {
        'source': 'devices'
    },
    'item_url': device_settings['item_url'],
    'embedded_fields': device_settings['embedded_fields'],
    'extra_response_fields': ['@type', 'hid', 'pid'],
    'etag_ignore_fields': device_settings['etag_ignore_fields'] + ['parent']
}


def register_parent_devices(domain: dict):
    return register_sub_types(domain, 'app.device', ('Peripheral', 'Monitor', 'Mobile', 'Computer'))
