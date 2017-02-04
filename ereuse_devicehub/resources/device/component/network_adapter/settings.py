from ereuse_devicehub.resources.device.component.settings import Component, ComponentSubSettings
from ereuse_devicehub.resources.schema import UnitCodes


class NetworkAdapter(Component):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.speed = {
            'type': 'float',
            'unitCode': UnitCodes.mbps,
            'sink': 1
        }


# network_adapter['serialNumber']['regex'] = '^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
# todo change test inputs so we can use it again

class NetworkAdapterSettings(ComponentSubSettings):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.schema = NetworkAdapter
