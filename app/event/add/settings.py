__author__ = 'Xavier Bustamante Talavera'
from app.event.settings import event, event_settings

add = dict(event, **{
    'components': {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'devices',
                'field': '_id',
                'embeddable': True
            }
        }
    }
})

add_settings = {
    'resource_methods': ['GET', 'POST'],
    'schema': add,
    'datasource': {
        'source': 'events',
        'filter': {'@type': {'$eq': 'Add'}},
    },
    'url': event_settings['url'] + '/add'
}
