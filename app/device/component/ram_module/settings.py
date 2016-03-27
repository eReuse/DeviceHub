import copy

from app.device.component.settings import component, component_sub_settings
from app.schema import UnitCodes

ram_module = copy.deepcopy(component)
ram_module.update({
    'size': {
        'type': 'integer',
        'unitCode': UnitCodes.mbyte,
        'min': 1,
        'sink': 1
    },
    'speed': {
        'type': 'float',
        'unitCode': UnitCodes.mhz,
        'min': 1,
        'sink': -1
    }
})

ram_module_settings = copy.deepcopy(component_sub_settings)
ram_module_settings.update({
    'schema': ram_module
})
