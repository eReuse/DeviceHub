import copy
from app.Utils import register_sub_types
from app.event.Event import Event

__author__ = 'Xavier Bustamante Talavera'
from app.schema import thing

event = copy.deepcopy(thing)
event.update({
    'date': {  # User specified date when the event was triggered
        'type': 'datetime',
    },
    'secured': {
        'type': 'boolean',
        'default': False
    },
    'incidence': {
        'type': 'boolean',
        'default': False
    },
    'message': {
        'type': 'string'
    },
    'geo': {
        'type': 'point',
        'anyof': [{'required': True}, {'dependencies': ['place']}]  # me OR places
    },
    'byUser': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True
        },
        'readonly': True
    },
    'place': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'places',
            'field': '_id',
            'embeddable': True
        }
    }
})

event_with_one_device = copy.deepcopy(event)
event_with_one_device.update({
    'device': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        }
    }
})

event_with_devices = copy.deepcopy(event)
event_with_devices.update({
    'devices': {
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

event_settings = {
    'resource_methods': ['GET'],
    'schema': event,
    'allow_unknown': True,
    'embedded_fields': ['device', 'place'],
    'datasource': {
        'default_sort': [('_created', -1)]
    },
    'url': 'events'
    #'url': 'devices/<regex("[a-f0-9]{24}"):device>/events',
}

event_sub_settings = {
    'item_methods': [],
    'datasource': {
        'source': 'events',
        'default_sort': [('_created', -1)]
    },
    #'url': event_settings['url'] + '/'
    'url': 'devices/<regex("[a-f0-9]{24}"):device>/events/'
}

event_sub_settings_one_device = copy.deepcopy(event_sub_settings)
event_sub_settings_one_device.update({
    'embedded_fields': ['device']
})

event_sub_settings_multiple_devices = copy.deepcopy(event_sub_settings)
event_sub_settings_one_device.update({
    'resource_methods': ['POST'],
    'item_methods': ['PATCH', 'DELETE'],
    'embedded_fields': ['devices']
})

def register_events(domain: dict):
    register_sub_types(domain, 'app.event', Event.get_types())
