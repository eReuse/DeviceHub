import copy

from app.device.benchmark_settings import union_of_benchmarks
from app.device.schema import Device
from app.device.settings import device_settings, device_sub_settings, DeviceSettings, DeviceSubSettings


class Component(Device):
    interface = {
        'type': 'string',
        'teaser': False,
        'sink': -1
    }
    parent = {
        'type': 'string',
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        }
    }

    @classmethod
    def subclasses_attributes(cls):
        global_types = super().subclasses_attributes()
        global_types['size']['type'] = global_types['speed']['type'] = 'number'
        global_types['erasure']['schema']['@type']['allowed'] = 'EraseSectors', 'EraseBasic'
        global_types['benchmark']['schema'] = union_of_benchmarks
        return global_types


class ComponentSettings(DeviceSettings):
    _schema = Component


class ComponentSubSettings(DeviceSubSettings):
    pass
