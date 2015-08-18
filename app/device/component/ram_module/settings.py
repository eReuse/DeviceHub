__author__ = 'Xavier Bustamante Talavera'
from app.device.settings import device

ram_module = dict(device, **{
    'clock': {  # In Mhz
        'type': float,
        'min': 1
    },
    'size': {  # In Megabytes
        'type': float,
        'min': 1
    }
})

ram_module_settings = {
    'internal_resource': True,
    'schema': ram_module
}
