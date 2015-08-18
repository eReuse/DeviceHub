__author__ = 'Xavier Bustamante Talavera'
from app.device.settings import device

processor = dict(device, **{
    'numberOfCores': {
        'type': int,
        'min': 1,
    },
    'speed': {  # In Ghz
        'type': float
    },
    'busClock': {
        'type': float,
    },
    'address': {  # In bytes
        'type': int,
        'allowed': [8, 16, 32, 64, 128, 256]
    },
})

processor_settings = {
    'internal_resource': True,
    'schema': processor
}
