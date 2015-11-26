import copy

from app.utils import register_sub_types
from app.schema import thing

HID_REGEX = '[\w]+-[\w]+'

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
        'unique': True
    },
    'icon': {
        'type': 'string',
        'readonly': True
    },
    'hid': {
        'type': 'hid',
        # 'regex': HID_REGEX, They are executed by type hid
        # 'unique': True
    },
    'pid': {
        'type': 'string',
        'unique': True
    },
    'isUidSecured': {
        'type': 'boolean',
        'default': True
    },
    'components': {
        'type': 'list',
        'schema': {
            'type': 'objectid',
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
    'embedded_fields': ['components'],
    'url': 'devices',
    'etag_ignore_fields': ['hid', '_id', 'components', 'isUidSecured', '_created', '_updated', '_etag', 'speed',
                           'busClock']
}

device_sub_settings = {
    'resource_methods': ['POST'],
    'item_methods': ['DELETE'],
    'url': device_settings['url'] + '/',
    'datasource': {
        'source': 'devices'
    },
    'embedded_fields': device_settings['embedded_fields'],
    'extra_response_fields': ['@type', 'hid', 'pid'],
    'etag_ignore_fields': device_settings['etag_ignore_fields'] + ['parent']
}


def register_parent_devices(domain: dict):
    return register_sub_types(domain, 'app.device', ('Computer',))
