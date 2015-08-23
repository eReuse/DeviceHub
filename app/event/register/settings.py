__author__ = 'Xavier Bustamante Talavera'
from app.event.settings import event, event_sub_settings

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

register_settings = dict(event_sub_settings, **{
    'schema': register,
    'url': event_sub_settings['url'] + 'register'
})
