from app.device.schema import Device
from app.device.settings import DeviceSubSettings


class Monitor(Device):
    type = {
        'type': 'string',
        'allowed': {'TFT', 'LCD'}
    }
    inches = {
        'type': 'natural'
    }


class MonitorSettings(DeviceSubSettings):
    _schema = Monitor