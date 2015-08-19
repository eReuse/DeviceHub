__author__ = 'Xavier Bustamante Talavera'
from app.schema import thing
HID_REGEX = '^([\w]*-){1}[\w]*$'

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
    'resource_methods': ['GET', 'POST'],
    'schema': device,
    'additional_lookup': {
        'field': 'hid',
        'url': 'regex("' + HID_REGEX + '")'
    },
    'url': 'devices'
}
