import copy

from app.device.settings import device, device_sub_settings

peripheral = copy.deepcopy(device)
peripheral.update({
    'type': {
        'type': 'string',
        'allowed': ['Router', 'Switch', 'Printer', 'Scanner', 'MultifunctionPrinter', 'Terminal', 'HUB', 'SAI', 'Keyboard', 'Mouse']
    }
})

peripheral_settings = copy.deepcopy(device_sub_settings)
peripheral_settings.update({
    'schema': peripheral,
    'url': device_sub_settings['url'] + 'peripheral'
})
