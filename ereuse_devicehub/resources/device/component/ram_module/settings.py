from ereuse_devicehub.resources.device.component.settings import Component, ComponentSubSettings
from ereuse_devicehub.resources.schema import UnitCodes


class RamModule(Component):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.size = {
            'type': 'integer',
            'unitCode': UnitCodes.mbyte,
            'min': 1,
            'sink': 1
        }
        self.speed = {
            'type': 'float',
            'unitCode': UnitCodes.mhz,
            'min': 1,
            'sink': -1
        }


class RamModuleSettings(ComponentSubSettings):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.schema = RamModule
