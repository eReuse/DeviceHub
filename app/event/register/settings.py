__author__ = 'Xavier Bustamante Talavera'
from app.event.settings import event, event_settings

register = dict(event, **{
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

register_settings = {
    'resource_methods': ['GET', 'POST'],
    'schema': register,
    'datasource': {
        'source': 'events',
        'filter': {'@type': {'$eq': 'Register'}},
    },
    'url': event_settings['url'] + '/register'
}
