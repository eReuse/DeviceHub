from ereuse_devicehub.resources.device.benchmark_settings import BenchmarkProcessor
from ereuse_devicehub.resources.device.component.settings import Component, ComponentSubSettings
from ereuse_devicehub.resources.schema import UnitCodes


class Processor(Component):
    numberOfCores = {
        'type': 'integer',
        'min': 1,
        'sink': 1
    }
    speed = {
        'type': 'float',
        'unitCode': UnitCodes.ghz,
        'sink': 1
    }
    address = {
        'type': 'integer',
        'unitCode': UnitCodes.bit,
        'allowed': {8, 16, 32, 64, 128, 256},
        'sink': -1
    }
    benchmark = {
        'type': 'dict',
        'schema': BenchmarkProcessor,
        'writeonly': True,
    }
    benchmarks = {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': BenchmarkProcessor
        },
        'readonly': True
    }


class ProcessorSettings(ComponentSubSettings):
    _schema = Processor
