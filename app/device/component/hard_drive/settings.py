__author__ = 'Xavier Bustamante Talavera'
from app.device.settings import device

hard_drive = dict(device, **{
    'interface': {
        'type': 'string',
    },
    'size': {  # In Megabytes
        'type': float
    }
})

hard_drive_settings = {
    'internal_resource': True,
    'schema': hard_drive
}
