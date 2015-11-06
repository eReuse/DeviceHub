import copy

__author__ = 'Xavier Bustamante Talavera'
from app.device.component.settings import component, component_sub_settings

network_adapter = copy.deepcopy(component)
network_adapter_settings = copy.deepcopy(component_sub_settings)

network_adapter.update({
    'speed': {      # Speed in MB
        'type': 'integer',
        'allowed': [10, 100, 1000, 10000]
    }
})

network_adapter_settings.update({
    'schema': network_adapter,
    'url': component_sub_settings['url'] + 'network-adapter'
})
