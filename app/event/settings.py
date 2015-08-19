__author__ = 'Xavier Bustamante Talavera'
from app.schema import thing

event = dict(thing, **{
    'date': {
        'type': 'datetime'
    },
    'secured': {
        'type': 'boolean'
    },
    'incidence': {
        'type': 'boolean'
    },
    'device': {
        'type': 'objectid',
             'data_relation': {
                'resource': 'devices',
                'field': '_id',
                'embeddable': True
            }
    }
})

event_settings = {
    'resource_methods': ['GET', 'POST'],
    'schema': event,
    'url': 'devices/<regex("[a-f0-9]{24}"):device>/events',
}
