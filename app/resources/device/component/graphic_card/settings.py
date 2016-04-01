from app.resources.device.component.settings import Component, ComponentSubSettings
from app.resources.schema import UnitCodes


class GraphicCard(Component):
    memory = {
        'type': 'float',
        'unitCode': UnitCodes.mbyte,  # MB
        'min': 1,
        'sink': 3
    }


class GraphicCardSettings(ComponentSubSettings):
    _schema = GraphicCard

