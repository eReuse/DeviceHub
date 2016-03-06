import copy

from app.device.benchmark_settings import benchmark_processor
from app.device.component.settings import component, component_sub_settings
from app.schema import UnitCodes
processor = copy.deepcopy(component)
processor_settings = copy.deepcopy(component_sub_settings)

processor.update({
    'numberOfCores': {
        'type': 'integer',
        'min': 1,
        'sink': 1
    },
    'speed': {
        'type': 'float',
        'unitCode': UnitCodes.ghz,
        'sink': 1
    },
    'address': {
        'type': 'integer',
        'unitCode': UnitCodes.bit,
        'allowed': [8, 16, 32, 64, 128, 256],
        'sink': -1
    },
    'benchmark': {
        'type': 'dict',
        'schema': copy.deepcopy(benchmark_processor),
        'writeonly': True,
    },
    'benchmarks': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': copy.deepcopy(benchmark_processor)
        },
        'readonly': True
    }
})
processor_settings.update({
    'schema': processor,
    'url': component_sub_settings['url'] + 'processor'
})
