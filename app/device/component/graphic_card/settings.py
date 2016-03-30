import copy

from app.device.component.settings import component_sub_settings, Component, ComponentSubSettings
from app.schema import UnitCodes

graphic_card_settings = copy.deepcopy(component_sub_settings)


class GraphicCard(Component):
    memory = {
        'type': 'float',
        'unitCode': UnitCodes.mbyte,  # MB
        'min': 1,
        'sink': 3
    }


class GraphicCardSettings(ComponentSubSettings):
    _schema = GraphicCard


a = 2