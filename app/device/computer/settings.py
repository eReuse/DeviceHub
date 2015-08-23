__author__ = 'Xavier Bustamante Talavera'
from app.device.settings import device, device_sub_settings

computer = dict(device, **{
    'type': {
        'type': 'string',
        'allowed': ['Desktop', 'Laptop', 'Netbook', 'Server', 'Microtower']
    },
    'totalMemory': {  # In Gigabytes
        'type': 'float'
    }
})

computer_settings = dict(device_sub_settings, **{
    'schema': computer,
    'url': device_sub_settings['url'] + 'computer'
})
