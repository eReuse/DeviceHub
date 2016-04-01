from app.resources.device.schema import Device
from app.resources.device.settings import DeviceSubSettings


class Peripheral(Device):
    type = {
        'type': 'string',
        'allowed': {'Router', 'Switch', 'Printer', 'Scanner', 'MultifunctionPrinter', 'Terminal', 'HUB', 'SAI',
                    'Keyboard', 'Mouse'}
    }


class PeripheralSettings(DeviceSubSettings):
    _schema = Peripheral