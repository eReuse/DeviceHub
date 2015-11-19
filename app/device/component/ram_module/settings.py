import copy

from app.device.component.settings import component, component_sub_settings

ram_module = copy.deepcopy(component)
ram_module.update({
    'clock': {  # In Mhz
                'type': 'float',
                'min': 1
                },
    'size': {  # In Megabytes
               'type': 'float',
               'min': 1
    },
    'speed': {
        'type': 'integer',
        'min': 1
    }
})

ram_module_settings = copy.deepcopy(component_sub_settings)
ram_module_settings.update({
    'schema': ram_module,
    'url': component_sub_settings['url'] + 'ram-module'
})
