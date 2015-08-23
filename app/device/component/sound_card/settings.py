__author__ = 'Xavier Bustamante Talavera'
from app.device.component.settings import component, component_sub_settings

sound_card_settings = dict(component_sub_settings, **{
    'schema': component,
    'url': component_sub_settings['url'] + 'sound-card'
})
