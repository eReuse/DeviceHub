import copy

from app.device.component.settings import component_sub_settings, Component, ComponentSubSettings
from app.schema import UnitCodes

network_adapter_settings = copy.deepcopy(component_sub_settings)


class NetworkAdapter(Component):
    speed = {
        'type': 'float',
        'unitCode': UnitCodes.mbps,
        'sink': 1
    }


# network_adapter['serialNumber']['regex'] = '^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$' todo change test inputs so we can use it again

class NetworkAdapterSettings(ComponentSubSettings):
    _schema = NetworkAdapter

