__author__ = 'Xavier Bustamante Talavera'
from app.device.settings import device

computer = dict(device, **{
    'type': {
        'type': 'string',
        'allowed': ['Desktop', 'Laptop', 'Netbook', 'Server', 'Microtower']
    },
    'totalMemory': {  # In Gigabytes
        'type': float
    }
})

computer_settings = {
    'resource_methods': ['POST'],
    'schema': computer
}
