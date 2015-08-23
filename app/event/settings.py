from app.Utils import register_sub_types
from app.event.Event import Event

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
    'allow_unknown': True,
    'url': 'devices/<regex("[a-f0-9]{24}"):device>/events',
}

event_sub_settings = {
    'resource_methods': ['GET', 'POST'],
    'datasource': {
        'source': 'events',
        'filter': {'@type': {'$eq': 'Add'}},
    },
    'url': event_settings['url'] + '/'
}

def register_events(domain: dict):
    register_sub_types(domain, 'app.event', Event.get_types())
