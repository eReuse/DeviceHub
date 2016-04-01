from app.resources.device.schema import Device
from app.resources.device.settings import DeviceSubSettings


class Mobile(Device):
    type = {
        'type': 'string',
        'allowed': {'Smartphone', 'Tablet'}
    }
    imei = {
        'type': 'string',
        'unique': True
    }
    meid = {
        'type': 'string',
        'unique': True
    }


class MobileSettings(DeviceSubSettings):
    _schema = Mobile