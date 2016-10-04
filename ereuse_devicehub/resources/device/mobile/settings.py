import copy

from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.device.settings import DeviceSubSettings


class Mobile(Device):
    imei = {
        'type': 'string',
        'unique': True
    }
    meid = {
        'type': 'string',
        'unique': True
    }
    type = {
        'type': 'string',
        'allowed': {'Smartphone', 'Tablet'},
        'required': True
    }
    manufacturer = copy.copy(Device.manufacturer)
    manufacturer['required'] = True
    serialNumber = copy.copy(Device.serialNumber)
    serialNumber['required'] = True
    model = copy.copy(Device.model)
    model['required'] = True


class MobileSettings(DeviceSubSettings):
    _schema = Mobile
