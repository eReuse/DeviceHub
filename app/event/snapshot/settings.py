__author__ = 'Xavier Bustamante Talavera'
from app.event.settings import event, event_sub_settings
from app.device.computer.settings import computer

snapshot = dict(event, **{
    'offline': {
        'type': 'boolean'
    },
    'automatic': {
        'type': 'boolean'
    },
    'version': {
        'type': 'float',
    },
    'device': {
        'type': 'dict',
        'schema': computer
    },

    'components': {
        'type': 'list',
        'schema': {
            'type': 'dict',
        }
    }
})

snapshot_settings = dict(event_sub_settings, **{
    'schema': snapshot,
    'url': 'snapshot',
})
