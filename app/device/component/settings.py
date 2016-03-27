import copy

from app.device.benchmark_settings import union_of_benchmarks
from app.device.settings import device, device_settings, device_sub_settings
from .component import Component

component = copy.deepcopy(device)
component.update({
    'interface': {
        'type': 'string',
        'teaser': False,
        'sink': -1
    },
    'parent': {
        'type': 'string',
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        }
    }
})
component_sub_settings = copy.deepcopy(device_sub_settings)


def merge_hook(app, resource, own_settings, superclasses):
    global_types = own_settings['schema']
    global_types['size']['type'] = global_types['speed']['type'] = 'number'
    global_types['erasure']['schema']['@type']['allowed'] = 'EraseSectors', 'EraseBasic'
    global_types['benchmark']['schema'] = union_of_benchmarks
    app.update_resource(resource, own_settings)  # This does not update the parents

component_settings = {
    'resource_methods': device_settings['resource_methods'],
    'additional_lookup': device_settings['additional_lookup'],
    'schema': component,
    'is_super_class_of': {
        'modules': Component.get_types_of_components()
    },
    'merge_hook': merge_hook
}

