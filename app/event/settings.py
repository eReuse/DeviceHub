import copy

from app.Utils import register_sub_types
from app.event.Event import Event
from app.schema import thing

"""
Event Settings file.

It is divided in:
- Event schema and settings
- Subevent schema and settings:
    - Subevents attached to one device
    - Subevents attached to multiple devices
"""

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
event_settings = {
    'resource_methods': ['GET'],
    'schema': None,  # We update the schema in DOMAIN
    'embedded_fields': ['device', 'place', 'devices', 'places', 'components'],
    'datasource': {
        'source': 'events',
        'default_sort': [('_created', -1)]
    },
    'url': 'events'
}
event_sub_settings = {
    'item_methods': [],
    'datasource': event_settings['datasource'],
    'url': event_settings['url'] + '/'
}

event_with_one_device = copy.deepcopy(event)
event_with_one_device.update({
    'device': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        },
        'required': True
    }
})
event_sub_settings_one_device = copy.deepcopy(event_sub_settings)
event_sub_settings_one_device.update({
    'embedded_fields': ['device']
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
        },
        'required': True
    }
})
event_sub_settings_multiple_devices = copy.deepcopy(event_sub_settings)
event_sub_settings_multiple_devices.update({
    'resource_methods': ['POST'],
    'item_methods': ['PATCH', 'DELETE'],
    'embedded_fields': ['devices']
})


def register_events(domain: dict):
    """
    Register the subevents and generates the full event schema to insert it to Event Resource
    :param domain: Full domain dict
    :return:
    """
    return register_sub_types(domain, 'app.event', Event.get_types())
