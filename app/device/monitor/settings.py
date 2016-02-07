import copy

from app.device.settings import device, device_sub_settings

monitor = copy.deepcopy(device)
monitor.update({
    'type': {
        'type': 'string',
        'allowed': ['TFT', 'LCD']
    },
    'inches': {
        'type': 'natural'
    }
})

monitor_settings = copy.deepcopy(device_sub_settings)
monitor_settings.update({
    'schema': monitor,
    'url': device_sub_settings['url'] + 'monitor'
})
