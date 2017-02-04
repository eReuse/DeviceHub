from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.device.settings import DeviceSubSettings
from ereuse_devicehub.resources.schema import UnitCodes


class Computer(Device):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.type = {
            'type': 'string',
            'allowed': {'Desktop', 'Laptop', 'Netbook', 'Server', 'Microtower'}
        }
        self.forceCreation = {
            'type': 'boolean',
            'default': False
        }
        self.totalRamSize = {
            'type': 'float',
            'materialized': True,
            'description': 'The total amount of RAM memory the computer has.',
            'doc': 'It is updated after a Register, Add o Remove',
            'short': 'RAM',
            'unitCode': UnitCodes.gbyte,
            'default': 0,
            'sink': 1
        }
        self.processorModel = {
            'type': 'string',
            'materialized': True,
            'description': 'The model of the processor.',
            'short': 'CPU',
            'sink': 1
        }
        self.totalHardDriveSize = {
            'type': 'float',
            'materialized': True,
            'description': 'The total amount of hard-drive capacity the computer has.',
            'short': 'Capacity',
            'unitCode': UnitCodes.mbyte,
            'default': 0,
            'sink': 1
        }


class ComputerSettings(DeviceSubSettings):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.schema = Computer
        self.etag_ignore_fields = parent.etag_ignore_fields + ['forceCreation', 'totalRamSize',
                                                                          'processorModel',
                                                                          'totalHardDriveSize']
