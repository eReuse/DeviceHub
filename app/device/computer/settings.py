import copy

from app.device.component.settings import ComponentSubSettings
from app.device.schema import Device
from app.device.settings import device_sub_settings, DeviceSubSettings


class Computer(Device):
    type = {
        'type': 'string',
        'allowed': ['Desktop', 'Laptop', 'Netbook', 'Server', 'Microtower']
    }
    forceCreation = {
        'type': 'boolean',
        'default': False
    }


class ComputerSettings(DeviceSubSettings):
    _schema = Computer
    etag_ignore_fields = DeviceSubSettings.etag_ignore_fields + ['forceCreation']
