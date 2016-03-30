import copy

from app.device.benchmark_settings import benchmark_processor
from app.device.component.settings import component_sub_settings, Component, ComponentSubSettings
from app.schema import UnitCodes

processor_settings = copy.deepcopy(component_sub_settings)


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
        'allowed': [8, 16, 32, 64, 128, 256],
        'sink': -1
    }
    benchmark = {
        'type': 'dict',
        'schema': copy.deepcopy(benchmark_processor),
        'writeonly': True,
    }
    benchmarks = {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': copy.deepcopy(benchmark_processor)
        },
        'readonly': True
    }


class ProcessorSettings(ComponentSubSettings):
    _schema = Processor
