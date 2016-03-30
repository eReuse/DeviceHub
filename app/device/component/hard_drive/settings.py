from app.device.benchmark_settings import BenchmarkHardDrive
from app.device.component.settings import Component, ComponentSubSettings
from app.event.erase_basic.settings import EraseBasic
from app.event.test_hard_drive.settings import TestHardDrive
from app.schema import UnitCodes


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
        'schema': EraseBasic,
        'writeonly': True
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
        'schema': TestHardDrive
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
        'schema': BenchmarkHardDrive,
        'writeonly': True
    }
    benchmarks = {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': BenchmarkHardDrive
        },
        'readonly': True
    }

    @classmethod
    def _clean(cls, full_dict):
        full_dict = super(HardDrive, cls)._clean(full_dict)
        # todo We need to add this because these events are taken from hardDrive in snapshot,
        # We should remove them in Device POST, so they don't pass through the API and get generated.
        # This fields are generated automatically by the API
        del full_dict['erasure']['schema']['incidence']['default']
        del full_dict['erasure']['schema']['secured']['default']
        del full_dict['test']['schema']['incidence']['default']
        del full_dict['test']['schema']['secured']['default']
        full_dict['test']['schema']['device']['required'] = False
        full_dict['erasure']['schema']['device']['required'] = False

        return full_dict



class HardDriveSettings(ComponentSubSettings):
    _schema = HardDrive
    etag_ignore_fields = ComponentSubSettings.etag_ignore_fields + ['tests', 'erasures', 'test', 'erasure']
