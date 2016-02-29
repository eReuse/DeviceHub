import copy

from app.device.benchmark_settings import benchmark_hard_drive
from app.device.component.settings import component, component_sub_settings
from app.event.erase_basic.settings import erase_basic
from app.event.test_hard_drive.settings import test_hard_drive
from app.schema import UnitCodes

hard_drive = copy.deepcopy(component)
hard_drive_settings = copy.deepcopy(component_sub_settings)

hard_drive.update({
    'interface': {
        'type': 'string',
    },
    'size': {
        'type': 'float',
        'unitCode': UnitCodes.mbyte
    },
    'erasure': {
        'type': 'dict',
        'schema': copy.deepcopy(erase_basic)
    },
    'erasures': {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'events',
                'field': '_id',
                'embeddable': True
            }
        },
        'readonly': True
    },
    'firmwareRevision': {
        'type': 'string'
    },
    'blockSize': {
        'type': 'integer',
    },
    'sectors': {
        'type': 'integer'
    },
    'test': {
        'type': 'dict',
        'schema': copy.deepcopy(test_hard_drive),
    },
    'tests': {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'events',
                'field': '_id',
                'embeddable': True
            }
        },
        'readonly': True
    },
    'benchmark': {
        'type': 'dict',
        'schema': copy.deepcopy(benchmark_hard_drive),
        'writeonly': True
    },
    'benchmarks': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': copy.deepcopy(benchmark_hard_drive)
        },
        'readonly': True
    }
})
hard_drive['test']['schema']['device']['required'] = False
hard_drive['erasure']['schema']['device']['required'] = False
del hard_drive['erasure']['schema']['incidence']['default']
del hard_drive['erasure']['schema']['secured']['default']
del hard_drive['test']['schema']['incidence']['default']
del hard_drive['test']['schema']['secured']['default']
hard_drive_settings.update({
    'schema': hard_drive,
    'url': component_sub_settings['url'] + 'hard-drive',
    'etag_ignore_fields': hard_drive_settings['etag_ignore_fields'] + ['tests', 'erasures', 'test', 'erasure']
})

