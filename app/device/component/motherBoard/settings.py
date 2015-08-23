__author__ = 'busta'
from app.device.component.settings import component, component_sub_settings

motherboard_settings = dict(component_sub_settings, **{
    'schema': component,
    'url': component_sub_settings['url'] + 'motherboard'
})
