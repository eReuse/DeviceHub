from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.device.settings import DeviceSubSettings
from ereuse_devicehub.resources.schema import UnitCodes


class Computer(Device):
    type = {
        'type': 'string',
        'allowed': {'Desktop', 'Laptop', 'Netbook', 'Server', 'Microtower'}
    }
    forceCreation = {
        'type': 'boolean',
        'default': False
    }
    totalRamSize = {
        'type': 'float',
        'materialized': True,
        'description': 'The total amount of RAM memory the computer has.',
        'doc': 'It is updated after a Register, Add o Remove',
        'short': 'RAM',
        'unitCode': UnitCodes.gbyte,
        'default': 0,
        'sink': 1
    }
    processorModel = {
        'type': 'string',
        'materialized': True,
        'description': 'The model of the processor.',
        'short': 'CPU',
        'sink': 1
    }
    totalHardDriveSize = {
        'type': 'float',
        'materialized': True,
        'description': 'The total amount of hard-drive capacity the computer has.',
        'short': 'HDD',
        'unitCode': UnitCodes.mbyte,
        'default': 0,
        'sink': 1
    }


class ComputerSettings(DeviceSubSettings):
    _schema = Computer
    etag_ignore_fields = DeviceSubSettings.etag_ignore_fields + ['forceCreation', 'totalRamSize', 'processorModel',
                                                                 'totalHardDriveSize']
