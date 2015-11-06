import copy

__author__ = 'Xavier Bustamante Talavera'
from app.device.component.settings import component, component_sub_settings

hard_drive = copy.deepcopy(component)
hard_drive_settings = copy.deepcopy(component_sub_settings)

hard_drive.update({
    'interface': {
        'type': 'string',
    },
    'size': {  # In Megabytes
        'type': 'float'
    }
})
hard_drive_settings.update({
    'schema': hard_drive,
    'url': component_sub_settings['url'] + 'hard-drive'
})
