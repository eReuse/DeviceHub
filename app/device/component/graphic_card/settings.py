import copy

from app.device.component.settings import component, component_sub_settings
from app.schema import UnitCodes

graphic_card = copy.deepcopy(component)
graphic_card_settings = copy.deepcopy(component_sub_settings)

graphic_card.update({
    'memory': {
        'type': 'float',
        'unitCode': UnitCodes.mbyte,  # MB
        'min': 1,
        'sink': 3
    }
})

graphic_card_settings.update({
    'schema': graphic_card,
})
