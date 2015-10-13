from app.Utils import register_sub_types
from app.device.component.Component import Component

__author__ = 'Xavier Bustamante Talavera'
from app.schema import thing

HID_REGEX = '[\w]+-[\w]+'

product = dict(thing, **{
    'model': {
        'type': 'string'
    },
    'weight': {  # In kilograms
        'type': 'float',
    },
    'width': {  # In meters
        'type': 'float'
    },
    'height': {  # In meters
        'type': 'float'
    },
    'manufacturer': {
        'type': 'string'
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

device = dict(individualProduct, **{
    '_id': {
        'type': 'string'
    },
    'hid': {
        'type': 'string',
        'regex': HID_REGEX
    },
    'isUidSecured': {
        'type': 'boolean'
    },
    'components': {
        'type': 'list',
        'schema': {
            'type': 'objectid'
        }
    }
})

device_settings = {
    'resource_methods': ['GET'],
    'schema': device,
    'allow_unknown': True,  # It let us get all the fields of any subtype of device
    'additional_lookup': {
        'field': 'hid',
        'url': 'regex("' + HID_REGEX + '")'
    },
    'url': 'devices'
}

device_sub_settings = {
    'resource_methods': ['POST'],
    'url': device_settings['url'] + '/',
    'datasource': {
        'source': 'devices'
    },
}


def register_parent_devices(domain: dict):
    register_sub_types(domain, 'app.device', ('computer',))