from app.resources.device.component.settings import Component, ComponentSubSettings
from app.resources.schema import UnitCodes


class RamModule(Component):
    size = {
        'type': 'integer',
        'unitCode': UnitCodes.mbyte,
        'min': 1,
        'sink': 1
    }
    speed = {
        'type': 'float',
        'unitCode': UnitCodes.mhz,
        'min': 1,
        'sink': -1
    }


class RamModuleSettings(ComponentSubSettings):
    _schema = RamModule