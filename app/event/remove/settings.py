__author__ = 'Xavier Bustamante Talavera'
from app.event.settings import event, event_sub_settings

remove = dict(event, **{
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

remove_settings = dict(event_sub_settings, **{
    'schema': remove,
    'url': event_sub_settings['url'] + 'remove'
})
remove_settings['datasource']['filter'] = {'@type': {'$eq': 'Remove'}}
