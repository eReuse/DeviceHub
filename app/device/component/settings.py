import copy

__author__ = 'Xavier Bustamante Talavera'
from app.device.settings import device, device_settings, device_sub_settings
from .Component import Component
from app.Utils import register_sub_types

component = copy.deepcopy(device)
component_sub_settings = copy.deepcopy(device_sub_settings)

component_settings = {
    'resource_methods': device_settings['resource_methods'],
    'additional_lookup': device_settings['additional_lookup'],
    'schema': component,
    'allow_unknown': True,
    'datasource': {
        'source': 'devices',
        'filter': {'@type': {'$in': Component.get_types_of_components()}}
    },
    'url': device_settings['url'] + '/components/<regex("[a-f0-9]{24}"):component>'
}
component_sub_settings.update({
    'datasource': component_settings['datasource']
})


def register_components(domain: dict):
    return register_sub_types(domain, 'app.device.component', Component.get_types_of_components())


