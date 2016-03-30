import copy

from app.device.schema import Device
from app.device.settings import device_sub_settings, DeviceSubSettings


class Monitor(Device):
    type = {
        'type': 'string',
        'allowed': ['TFT', 'LCD']
    }
    inches = {
        'type': 'natural'
    }


class MonitorSettings(DeviceSubSettings):
    _schema = Monitor