import copy

from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.device.settings import DeviceSubSettings


class Peripheral(Device):
    type = {
        'type': 'string',
        'allowed': {
            'Router', 'Switch', 'Printer', 'Scanner', 'MultifunctionPrinter', 'Terminal', 'HUB',
            'SAI', 'Keyboard', 'Mouse', 'WirelessAccessPoint', 'LabelPrinter', 'Projector',
            'VideoconferenceDevice', 'SoundDevice', 'Microphone', 'WirelessMicrophone',
            'Scaler', 'VideoScaler', 'MemoryCardReader', 'Amplifier', 'AudioAmplifier'
        },
        'required': True
    }
    manufacturer = copy.copy(Device.manufacturer)
    manufacturer['required'] = True
    serialNumber = copy.copy(Device.serialNumber)
    serialNumber['required'] = True
    model = copy.copy(Device.model)
    model['required'] = True


class PeripheralSettings(DeviceSubSettings):
    _schema = Peripheral
