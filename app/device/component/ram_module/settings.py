__author__ = 'Xavier Bustamante Talavera'
from app.device.component.settings import component, component_sub_settings

ram_module = dict(component, **{
    'clock': {  # In Mhz
        'type': 'float',
        'min': 1
    },
    'size': {  # In Megabytes
        'type': 'float',
        'min': 1
    }
})

ram_module_settings = dict(component_sub_settings, **{
    'schema': ram_module,
    'url': component_sub_settings['url'] + 'ram-module'
})
