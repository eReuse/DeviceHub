import copy

from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.device.settings import DeviceSubSettings


class Mobile(Device):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.imei = {
            'type': 'string',
            'unique': True
        }
        self.meid = {
            'type': 'string',
            'unique': True
        }
        self.type = {
            'type': 'string',
            'allowed': {'Smartphone', 'Tablet'},
            'required': True
        }
        self.manufacturer = copy.copy(parent.manufacturer)
        self.manufacturer['required'] = True
        self.serialNumber = copy.copy(parent.serialNumber)
        self.serialNumber['required'] = True
        self.model = copy.copy(parent.model)
        self.model['required'] = True


class MobileSettings(DeviceSubSettings):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.schema = Mobile
