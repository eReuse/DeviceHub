import copy

from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.device.settings import DeviceSubSettings


class TelevisionSet(Device):
    type = {
        'type': 'string',
        'allowed': {'CRT', 'LCD', 'LED', 'OLED', 'Plasma'},
        'required': True
    }
    inches = {
        'type': 'natural'
    }
    manufacturer = copy.copy(Device.manufacturer)
    manufacturer['required'] = True
    serialNumber = copy.copy(Device.serialNumber)
    serialNumber['required'] = True
    model = copy.copy(Device.model)
    model['required'] = True


class TelevisionSetSettings(DeviceSubSettings):
    _schema = TelevisionSet
