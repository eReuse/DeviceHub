import copy

from app.device.component.settings import component, component_sub_settings

processor = copy.deepcopy(component)
processor_settings = copy.deepcopy(component_sub_settings)

processor.update({
    'numberOfCores': {
        'type': 'integer',
        'min': 1,
    },
    'speed': {
        'type': 'float'  # In Ghz
    },
    'busClock': {
        'type': 'integer',
    },
    'address': {
        'type': 'integer',  # In bytes
        'allowed': [8, 16, 32, 64, 128, 256]
    },
})
processor_settings.update({
    'schema': processor,
    'url': component_sub_settings['url'] + 'processor'
})
