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


class MobilePhone(Mobile):
    pass


class TabletComputer(Mobile):
    pass


class MobileSettings(DeviceSubSettings):
    _schema = Mobile
