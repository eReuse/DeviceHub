__author__ = 'Xavier Bustamante Talavera'
from app.device.component.settings import component, component_sub_settings

network_adapter = dict(component, **{
    'speed': {      # Speed in MB
        'type': 'integer',
        'allowed': [10, 100, 1000, 10000]
    }
})

network_adapter_settings = dict(component_sub_settings, **{
    'schema': network_adapter,
    'url': component_sub_settings['url'] + 'network-adapter'
})
