import copy

from app.device.component.settings import component, component_sub_settings
from app.schema import UnitCodes

network_adapter = copy.deepcopy(component)
network_adapter_settings = copy.deepcopy(component_sub_settings)

network_adapter.update({
    'speed': {
        'type': 'float',
        'unitCode': UnitCodes.mbps,
        'sink': 1
    }
})

#network_adapter['serialNumber']['regex'] = '^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$' todo change test inputs so we can use it again

network_adapter_settings.update({
    'schema': network_adapter
})
