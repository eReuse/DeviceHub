__author__ = 'Xavier Bustamante Talavera'
from app.device.component.settings import component, component_sub_settings

processor = dict(component, **{
    'numberOfCores': {
        'type': 'integer',
        'min': 1,
    },
    'speed': {  # In Ghz
        'type': 'float'
    },
    'busClock': {
        'type': 'float',
    },
    'address': {  # In bytes
        'type': 'integer',
        'allowed': [8, 16, 32, 64, 128, 256]
    },
})

processor_settings = dict(component_sub_settings, **{
    'schema': processor,
    'url': component_sub_settings['url'] + 'processor'
})
