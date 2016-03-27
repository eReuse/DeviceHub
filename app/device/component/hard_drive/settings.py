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
        'sink': -1,
        'teaser': False
    },
    'size': {
        'type': 'float',
        'unitCode': UnitCodes.mbyte,
        'sink': 1
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
        'type': 'string',
        'teaser': False,
        'sink': -1
    },
    'blockSize': {
        'type': 'integer',
        'sink': -1,
        'teaser': False
    },
    'sectors': {
        'type': 'integer',
        'sink': -1,
        'teaser': False
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
hard_drive['test']['schema']['@type']['allowed'] = ['TestHardDrive']
del hard_drive['erasure']['schema']['incidence']['default']
del hard_drive['erasure']['schema']['secured']['default']
del hard_drive['test']['schema']['incidence']['default']
del hard_drive['test']['schema']['secured']['default']
hard_drive_settings.update({
    'schema': hard_drive,
    'etag_ignore_fields': hard_drive_settings['etag_ignore_fields'] + ['tests', 'erasures', 'test', 'erasure']
})

