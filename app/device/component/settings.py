__author__ = 'Xavier Bustamante Talavera'
from app.device.settings import device, device_settings, device_sub_settings
from .Component import Component
from app.Utils import register_sub_types

component = dict(device)

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

component_sub_settings = dict(device_sub_settings, **{
    'datasource': component_settings['datasource']
})

def register_components(domain: dict):
    register_sub_types(domain, 'app.device.component', Component.get_types_of_components())


