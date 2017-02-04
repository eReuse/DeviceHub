import copy

from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.device.settings import DeviceSubSettings


class Peripheral(Device):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.type = {
            'type': 'string',
            'allowed': {'Router', 'Switch', 'Printer', 'Scanner', 'MultifunctionPrinter', 'Terminal', 'HUB', 'SAI',
                        'Keyboard', 'Mouse'},
            'required': True
        }
        self.manufacturer = copy.copy(parent.manufacturer)
        self.manufacturer['required'] = True
        self.serialNumber = copy.copy(parent.serialNumber)
        self.serialNumber['required'] = True
        self.model = copy.copy(parent.model)
        self.model['required'] = True



class PeripheralSettings(DeviceSubSettings):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.schema = Peripheral
