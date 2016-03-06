import copy

from app.device.benchmark_settings import Benchmark, union_of_benchmarks
from app.device.settings import device, device_settings, device_sub_settings
from app.utils import register_sub_types
from .component import Component

component = copy.deepcopy(device)
component.update({
    'interface': {
        'type': 'string',
        'teaser': False,
        'sink': -1
    },
    'parent': {
        'type': 'string'
    }
})
component_sub_settings = copy.deepcopy(device_sub_settings)

component_settings = {
    'resource_methods': device_settings['resource_methods'],
    'additional_lookup': device_settings['additional_lookup'],
    'schema': component,
    'datasource': {
        'source': 'devices',
        'filter': {'@type': {'$in': Component.get_types_of_components()}}
    },
    'url': device_settings['url'] + '/components/<regex("[a-f0-9]{24}"):component>',
}
component_sub_settings.update({
    'datasource': component_settings['datasource']
})


def register_components(domain: dict):
    global_types = register_sub_types(domain, 'app.device.component', Component.get_types_of_components())
    global_types['size']['type'] = global_types['speed']['type'] = 'number'
    global_types['erasure']['schema']['@type']['allowed'] = 'EraseSectors', 'EraseBasic'
    global_types['benchmark']['schema'] = union_of_benchmarks
    return global_types
