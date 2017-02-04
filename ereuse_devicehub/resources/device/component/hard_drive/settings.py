from ereuse_devicehub.resources.device.benchmark_settings import BenchmarkHardDrive
from ereuse_devicehub.resources.device.component.settings import Component, ComponentSubSettings
from ereuse_devicehub.resources.event.device.erase_basic.settings import EraseBasic
from ereuse_devicehub.resources.event.device.test_hard_drive.settings import TestHardDrive
from ereuse_devicehub.resources.schema import UnitCodes


class HardDrive(Component):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.interface = {
            'type': 'string',
            'sink': -1,
            'teaser': False
        }
        self.size = {
            'type': 'float',
            'unitCode': UnitCodes.mbyte,
            'sink': 1
        }
        self.erasure = {
            'type': 'dict',
            'schema': self.__proxy.generate_config_schema(EraseBasic),
            'writeonly': True
        }
        self.erasures = {
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
        self.firmwareRevision = {
            'type': 'string',
            'teaser': False,
            'sink': -1
        }
        self.blockSize = {
            'type': 'integer',
            'sink': -1,
            'teaser': False
        }
        self.sectors = {
            'type': 'integer',
            'sink': -1,
            'teaser': False
        }
        self.test = {
            'type': 'dict',
            'schema': self.__proxy.generate_config_schema(TestHardDrive)
        }
        self.tests = {
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
        self.benchmark = {
            'type': 'dict',
            'schema': self.__proxy.generate_config_schema(BenchmarkHardDrive),
            'writeonly': True
        }
        self.benchmarks = {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': self.__proxy.generate_config_schema(BenchmarkHardDrive)
            },
            'readonly': True
        }

    def actual_fields(self):
        fields = super().actual_fields()
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
    def config(self, parent=None):
        self.schema = HardDrive
        self.etag_ignore_fields = parent.etag_ignore_fields + ['tests', 'erasures', 'test', 'erasure']
