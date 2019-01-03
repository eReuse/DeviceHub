from ereuse_devicehub.resources.device.benchmark_settings import BenchmarkHardDrive
from ereuse_devicehub.resources.device.component.settings import Component, ComponentSubSettings
from ereuse_devicehub.resources.event.device.erase_basic.settings import EraseBasic
from ereuse_devicehub.resources.event.device.test_hard_drive.settings import TestHardDrive
from ereuse_devicehub.resources.schema import UnitCodes


class HardDrive(Component):
    type = {
        'type': 'string',
        'allowed': {'SSD', 'HDD'},
        'sink': 2,
        'teaser': True,
        'required': False
    }
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
        }
    }

    @classmethod
    def actual_fields(cls):
        fields = super().actual_fields()
        if cls._import_schemas:
            # todo We need to add this because these events are taken from hardDrive in snapshot,
            # We should remove them in Device POST, so they don't pass through the API and get generated.
            # This fields are generated automatically by the API
            del fields['erasure']['schema']['incidence']['default']
            del fields['erasure']['schema']['secured']['default']
            del fields['test']['schema']['incidence']['default']
            del fields['test']['schema']['secured']['default']
            fields['test']['schema']['device']['required'] = False
            fields['erasure']['schema']['device']['required'] = False
        return fields


class HardDriveSettings(ComponentSubSettings):
    _schema = HardDrive
    etag_ignore_fields = ComponentSubSettings.etag_ignore_fields + ['tests', 'erasures', 'test', 'erasure']
