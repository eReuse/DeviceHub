from ereuse_devicehub.resources.device.component.settings import Component, ComponentSubSettings
from ereuse_devicehub.resources.schema import UnitCodes


class GraphicCard(Component):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.memory = {
            'type': 'float',
            'unitCode': UnitCodes.mbyte,  # MB
            'min': 1,
            'sink': 3
        }


class GraphicCardSettings(ComponentSubSettings):
    def config(self, parent=None):
        self.schema = GraphicCard
