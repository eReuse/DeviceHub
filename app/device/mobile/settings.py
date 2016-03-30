import copy

from app.device.schema import Device
from app.device.settings import device_sub_settings


class Mobile(Device):
    type = {
        'type': 'string',
        'allowed': ['Smartphone', 'Tablet']
    }
    imei = {
        'type': 'string',
        'unique': True
    }
    meid = {
        'type': 'string',
        'unique': True
    }


class MobileSettings(MobileSubSettings):
    _schema = Mobile