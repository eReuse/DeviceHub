from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.device.settings import DeviceSubSettings


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
