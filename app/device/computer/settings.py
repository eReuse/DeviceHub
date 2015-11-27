import copy

from app.device.settings import device, device_sub_settings

computer = copy.deepcopy(device)
computer.update({
    'type': {
        'type': 'string',
        'allowed': ['Desktop', 'Laptop', 'Netbook', 'Server', 'Microtower']
    },
    'totalMemory': {
        'type': 'integer'  # In Gigabytes
    },
})

computer_settings = copy.deepcopy(device_sub_settings)
computer_settings.update({
    'schema': computer,
    'url': device_sub_settings['url'] + 'computer'
})
