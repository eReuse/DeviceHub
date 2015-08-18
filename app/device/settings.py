__author__ = 'Xavier Bustamante Talavera'
from app.common_schema import thing
HID_REGEX = '^([a-zA-Z0-9]*-){5}[a-zA-Z0-9]*$'

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

device = dict(thing, **{
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
    'additional_lookup': {
        'field': 'hid',
        'url': 'regex("' + HID_REGEX + '")'
    },
    'url': 'devices/<regex("[a-f0-9]{24}"):device>'
}
