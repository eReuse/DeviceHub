import copy

import pymongo

from app.schema import UnitCodes
from app.schema import thing
from app.utils import register_sub_types
from app.validation import HID_REGEX

product = dict(thing, **{
    'model': {
        'type': 'string',
        'sink': 4
    },
    'weight': {
        'type': 'float',
        'unitCode': UnitCodes.kgm,
        'sink': -1,
        'teaser': False
    },
    'width': {
        'type': 'float',
        'unitCode': UnitCodes.m,
        'sink': -1,
        'teaser': False
    },
    'height': {
        'type': 'float',
        'unitCode': UnitCodes.m,
        'sink': -1,
        'teaser': False
    },
    'manufacturer': {
        'type': 'string',
        'sink': 4

    },
    'productId': {
        'type': 'string',
        'sink': 3,
        'teaser': False
    }
})

individualProduct = dict(product, **{
    'serialNumber': {
        'type': 'string',
        'sink': 4
    }
})

device = copy.deepcopy(individualProduct)
device.update({
    '_id': {
        'type': 'string',
        'unique': True,
        'device_id': True,
        'sink': 4,
        'teaser': False
        # ALLOWED_WRITE_ROLES: Role.SUPERUSER  # For recovery purposes
    },
    'icon': {
        'type': 'string',
        'readonly': True,
        'teaser': False,
        'sink': -5
    },
    'hid': {
        'type': 'hid',
        'sink': 5,
        'teaser': False

    },
    'pid': {
        'type': 'string',
        'unique': True,
        'sink': 5
    },
    'isUidSecured': {
        'type': 'boolean',
        'default': True,
        'teaser': False
    },
    'labelId': {
        'type': 'string',  # Materialized label of the last snapshot
        'sink': 5
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
        'sink': 1,
        'default': []
    },
    'place': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'places',
            'embeddable': True,
            'field': '_id'
        },
        'readonly': True,  # Materialized
        'sink': 2
    },
    'owners': {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'accounts',
                'embeddable': True,
                'field': '_id'
            }
        },
        'readonly': True,  # Materialized
        'sink': 2
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
    'url': 'devices',
    'mongo_indexes': {
        '@type': [('@type', pymongo.DESCENDING)],
        '@type and subtype': [('@type', pymongo.DESCENDING), ('type', pymongo.DESCENDING)],
        '@type and _created': [('@type', pymongo.DESCENDING), ('_created', pymongo.DESCENDING)]
    },
    'etag_ignore_fields': ['hid', '_id', 'components', 'isUidSecured', '_created', '_updated', '_etag', 'speed',
                           'busClock', 'labelId', 'owners', 'place', 'benchmark', 'benchmarks'],
    'cache_control': 'max-age=1, must-revalidate'
}

device_sub_settings = {
    'resource_methods': ['POST'],
    'item_methods': ['DELETE'],
    'url': device_settings['url'] + '/',
    'datasource': {
        'source': 'devices'
    },
    'item_url': device_settings['item_url'],
    'extra_response_fields': ['@type', 'hid', 'pid'],
    'etag_ignore_fields': device_settings['etag_ignore_fields'] + ['parent'],
    'cache_control': device_settings['cache_control']
}


def register_parent_devices(domain: dict):
    return register_sub_types(domain, 'app.device', ('Peripheral', 'Monitor', 'Mobile', 'Computer'))
