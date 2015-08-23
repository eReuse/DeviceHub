__author__ = 'Xavier Bustamante Talavera'
from app.device.component.settings import component, component_sub_settings

graphic_card = dict(component, **{
    'memory': {      # Speed in MB
        'type': 'float',
        'min': 1,
    }
})

graphic_card_settings = dict(component_sub_settings, **{
    'schema': graphic_card,
    'url': component_sub_settings['url'] + 'graphic-card'
})
