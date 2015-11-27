import copy

from app.device.settings import device, device_sub_settings

mobile = copy.deepcopy(device)
mobile.update({
    'type': {
        'type': 'string',
        'allowed': ['Smartphone', 'Tablet']
    },
    'imei': {
        'type': 'string',
        'unique': True
    },
    'meid': {
        'type': 'string',
        'unique': True
    }
})

mobile_settings = copy.deepcopy(device_sub_settings)
mobile_settings.update({
    'schema': mobile,
    'url': device_sub_settings['url'] + 'mobile'
})
