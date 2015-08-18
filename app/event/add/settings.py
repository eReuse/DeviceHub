__author__ = 'Xavier Bustamante Talavera'
from app.event.settings import event, event_settings
from app.device.settings import device

snapshot = dict(event, **{
    'component': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        }
    }
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
