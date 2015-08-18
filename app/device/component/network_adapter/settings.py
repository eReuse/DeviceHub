__author__ = 'Xavier Bustamante Talavera'
from app.device.settings import device

network_adapter = dict(device, **{
    'speed': {      # Speed in MB
        'type': int,
        'allowed': [10, 100, 1000, 10000]
    }
})

network_adapter_settings = {
    'internal_resource': True,
    'schema': network_adapter
}
