import copy

__author__ = 'Xavier Bustamante Talavera'
from app.device.component.settings import component, component_sub_settings

sound_card_settings = copy.deepcopy(component_sub_settings)
sound_card_settings.update({
    'schema': component,
    'url': component_sub_settings['url'] + 'sound-card'
})
