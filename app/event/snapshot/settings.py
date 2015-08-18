__author__ = 'Xavier Bustamante Talavera'
from app.event.settings import event, event_settings
from app.device.settings import device

snapshot = dict(event, **{
    'offline': {
        'type': 'boolean'
    },
    'automatic': {
        'type': 'boolean'
    },
    'version': {
        'type': float,
    },
    'device': {
        'type': 'dict',
        'schema': device
    },
})

snapshot_settings = {
    'resource_methods': ['GET', 'POST'],
    'schema': snapshot,
    'datasource': {
        'source': 'events',
        'filter': {'@type': {'$eq': 'snapshot'}},
    },
    'url': event_settings.url + '/snapshot'
}
