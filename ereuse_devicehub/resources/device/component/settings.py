from ereuse_devicehub.resources.device.benchmark_settings import BenchmarkHardDrive, BenchmarkProcessor, Benchmark
from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.device.settings import DeviceSettings, DeviceSubSettings


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
    def subclasses_fields(cls):
        global_types = super(Component, cls).subclasses_fields()
        try:
            global_types['size']['type'] = global_types['speed']['type'] = 'number'
            global_types['erasure']['schema']['@type']['allowed'] = {'EraseSectors', 'EraseBasic'}
            union_of_benchmarks = BenchmarkHardDrive()
            union_of_benchmarks.update(BenchmarkProcessor())
            union_of_benchmarks['@type']['allowed'] = set(Benchmark.TYPES)
            global_types['benchmark']['schema'] = union_of_benchmarks
        except KeyError:
            pass
        return global_types


class ComponentSettings(DeviceSettings):
    _schema = Component


class ComponentSubSettings(DeviceSubSettings):
    _schema = False
