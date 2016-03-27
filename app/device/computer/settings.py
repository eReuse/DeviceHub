import copy

from app.device.settings import device, device_sub_settings

computer = copy.deepcopy(device)
computer.update({
    'type': {
        'type': 'string',
        'allowed': ['Desktop', 'Laptop', 'Netbook', 'Server', 'Microtower']
    },
    'forceCreation': {
        'type': 'boolean',
        'default': False
    }
})

computer_settings = copy.deepcopy(device_sub_settings)
computer_settings.update({
    'schema': computer,
    'etag_ignore_fields': computer_settings['etag_ignore_fields'] + ['forceCreation']
})
