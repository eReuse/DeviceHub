__author__ = 'Xavier Bustamante Talavera'
from app.device.settings import device

graphic_card = dict(device, **{
    'memory': {      # Speed in MB
        'memory': float,
        'min': 1,
    }
})

graphic_card_settings = {
    'internal_resource': True,
    'schema': graphic_card
}
