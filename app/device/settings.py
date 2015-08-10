__author__ = 'busta'
from app.common_schema import thing

device = dict(thing, **{
    'model': {
        'type': 'string'
    },
    'manufacturer': {
        'type': 'string'
    },
    'serialNumber': {
        'type': 'string'
    },
    'hid': {
        'type': 'string'
    },
})

device_settings = {
    'resource_methods': ['GET', 'POST'],
    'schema': device
}
