import copy

from app.device.component.settings import component, component_sub_settings

optical_drive = copy.deepcopy(component)
optical_drive_settings = copy.deepcopy(component_sub_settings)

optical_drive_settings.update({
    'schema': optical_drive,
    'url': component_sub_settings['url'] + 'optical-drive'
})
