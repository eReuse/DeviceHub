import copy

from app.device.benchmark_settings import benchmark_hard_drive
from app.device.component.settings import component_sub_settings, Component, ComponentSubSettings
from app.event.erase_basic.settings import EraseBasic
from app.event.test_hard_drive.settings import TestHardDrive
from app.schema import UnitCodes

hard_drive_settings = copy.deepcopy(component_sub_settings)


class HardDrive(Component):
    interface = {
        'type': 'string',
        'sink': -1,
        'teaser': False
    }
    size = {
        'type': 'float',
        'unitCode': UnitCodes.mbyte,
        'sink': 1
    }
    erasure = {
        'type': 'dict',
        'schema': EraseBasic()
    }
    erasures = {
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
    }
    firmwareRevision = {
        'type': 'string',
        'teaser': False,
        'sink': -1
    }
    blockSize = {
        'type': 'integer',
        'sink': -1,
        'teaser': False
    }
    sectors = {
        'type': 'integer',
        'sink': -1,
        'teaser': False
    }
    test = {
        'type': 'dict',
        'schema': TestHardDrive()
    }
    tests = {
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
    }
    benchmark = {
        'type': 'dict',
        'schema': copy.deepcopy(benchmark_hard_drive),
        'writeonly': True
    }
    benchmarks = {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': copy.deepcopy(benchmark_hard_drive)
        },
        'readonly': True
    }
HardDrive.test['schema']['device']['required'] = False
HardDrive.erasure['schema']['device']['required'] = False
HardDrive.test['schema']['@type']['allowed'] = ['TestHardDrive']
del HardDrive.erasure['schema']['incidence']['default']
del HardDrive.erasure['schema']['secured']['default']
del HardDrive.erasure['schema']['incidence']['default']
del HardDrive.erasure['schema']['secured']['default']


class HardDriveSettings(ComponentSubSettings):
    _schema = HardDrive
    etag_ignore_fields = ComponentSubSettings.etag_ignore_fields + ['tests', 'erasures', 'test', 'erasure']
