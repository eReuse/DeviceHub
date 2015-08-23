__author__ = 'Xavier Bustamante Talavera'
from app.device.component.settings import component, component_sub_settings

hard_drive = dict(component, **{
    'interface': {
        'type': 'string',
    },
    'size': {  # In Megabytes
        'type': 'float'
    }
})

hard_drive_settings = dict(component_sub_settings, **{
    'schema': hard_drive,
    'url': component_sub_settings['url'] + 'hard-drive'
})
