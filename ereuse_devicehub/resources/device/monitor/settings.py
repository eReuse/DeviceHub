import copy

from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.device.settings import DeviceSubSettings


class ComputerMonitor(Device):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.type = {
            'type': 'string',
            'allowed': {'TFT', 'LCD', 'LED', 'OLED'},
            'required': True
        }
        self.inches = {
            'type': 'natural'
        }
        self.manufacturer = copy.copy(parent.manufacturer)
        self.manufacturer['required'] = True
        self.serialNumber = copy.copy(parent.serialNumber)
        self.serialNumber['required'] = True
        self.model = copy.copy(parent.model)
        self.model['required'] = True


class MonitorSettings(DeviceSubSettings):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.schema = ComputerMonitor
