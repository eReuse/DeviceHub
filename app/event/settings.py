import copy

import pymongo

from app.event.event import Event
from app.schema import thing
from settings import EXTRA_RESPONSE_FIELDS

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
    'date': {
        'type': 'datetime',  # User specified date when the event was triggered
        'sink': -2,
        'description': 'When this happened. Leave blank if it is happening now'
    },
    'secured': {
        'type': 'boolean',
        'default': False,
        'sink': -3
    },
    'incidence': {
        'type': 'boolean',
        'default': False,
        'sink': -3,
        'description': 'Check if something went wrong, you can add details in a comment'
    },
    'comment': {
        'type': 'string',
        'sink': -4,
        'description': 'Short comment for fast and easy reading'
    },
    'geo': {
        'type': 'point',
        'sink': -5,
        'description': 'Where did it happened'
        # 'anyof': [{'required': True}, {'dependencies': ['place']}]  # me OR places
    },
    'byUser': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True
        },
        'readonly': True,
        'sink': 2
    },
    'byOrganization': {  # Materialization of the organization that, by the time of the event, the user worked in
        'type': 'string',
        'readonly': True
    }
})
place = {
    'place': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'places',
            'field': '_id',
            'embeddable': True
        },
        'sink': 0,
        'description': 'Where did it happened'
    }
}

# Materialized fields

# For add/remove, the user supplies this info. For allocate/locate/receive, this info is
# a readonly materialization of the the components of all the computers affected, to get an easier relationship
# between component - event when the event is performed to a parent
components = {
    'components': {
        'type': 'list',
        'schema': {
            'type': 'string',
            'data_relation': {
                'resource': 'devices',
                'field': '_id',
                'embeddable': True
            }
        },
        'description': 'Components affected by the event.'
    }
}
parent = {
    'parent': {
        'type': 'string',
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        },
        'description': 'The event triggered in this computer.'
    }
}

event_settings = {
    'resource_methods': ['GET'],
    'schema': event,  # We update the schema in DOMAIN
    'datasource': {
        'source': 'events',
        'default_sort': [('_created', -1)]
    },
    'mongo_indexes': {
        '@type': [('@type', pymongo.DESCENDING)],
        'device': [('device', pymongo.HASHED)],
        'components': [('components', pymongo.DESCENDING)],
    },
    'url': 'events',
    'cache_control': 'max-age=15, must-revalidate',
    'is_super_class_of': {
        'modules': Event.get_special_types(),
        'generic': Event.get_generic_types()
    }
}

event_sub_settings = {
    'item_methods': [],
    'datasource': event_settings['datasource'],
    'url': event_settings['url'] + '/',
    'extra_response_fields': EXTRA_RESPONSE_FIELDS,
    'cache_control': event_settings['cache_control']
}

event_with_one_device = copy.deepcopy(event)
event_with_one_device.update({
    'device': {
        'type': 'string',
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        },
        'required': True
    }
})
event_sub_settings_one_device = copy.deepcopy(event_sub_settings)

event_with_devices = copy.deepcopy(event)
event_with_devices.update({
    'devices': {
        'type': 'list',
        'schema': {
            'type': 'string',
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
    'item_methods': ['PATCH', 'DELETE']
})

event_settings['generic_schema'] = copy.deepcopy(event_sub_settings_multiple_devices)
event_settings['generic_schema']['schema'] = copy.deepcopy(event_with_devices)

