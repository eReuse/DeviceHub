import copy

from app.device.component.settings import component, component_sub_settings

ram_module = copy.deepcopy(component)
ram_module.update({
    'clock': {
        'type': 'integer',  # In Mhz
        'min': 1
    },
    'size': {
        'type': 'integer',  # In Megabytes
        'min': 1
    },
    'speed': {
        'type': 'float',
        'min': 1
    }
})

ram_module_settings = copy.deepcopy(component_sub_settings)
ram_module_settings.update({
    'schema': ram_module,
    'url': component_sub_settings['url'] + 'ram-module'
})
