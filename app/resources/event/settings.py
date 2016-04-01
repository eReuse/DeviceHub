import pymongo

from app.resources.schema import Thing
from app.resources.resource import ResourceSettings
from settings import EXTRA_RESPONSE_FIELDS


class Event(Thing):
    date = {
        'type': 'datetime',  # User specified date when the event was triggered
        'sink': -2,
        'description': 'When this happened. Leave blank if it is happening now'
    }
    secured = {
        'type': 'boolean',
        'default': False,
        'sink': -3
    }
    incidence = {
        'type': 'boolean',
        'default': False,
        'sink': -3,
        'description': 'Check if something went wrong, you can add details in a comment'
    }
    comment = {
        'type': 'string',
        'sink': -4,
        'description': 'Short comment for fast and easy reading'
    }
    geo = {
        'type': 'point',
        'sink': -5,
        'description': 'Where did it happened'
        # 'anyof': [{'required': True}, {'dependencies': ['place']}]  # me OR places
    }
    byUser = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True
        },
        'readonly': True,
        'sink': 2
    }
    byOrganization = {  # Materialization of the organization that, by the time of the event, the user worked in
        'type': 'string',
        'readonly': True
    }


class EventWithOneDevice(Event):
    device = {
        'type': 'string',
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        },
        'required': True
    }


class EventWithDevices(Event):
    devices = {
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


place = {
    'type': 'objectid',
    'data_relation': {
        'resource': 'places',
        'field': '_id',
        'embeddable': True
    },
    'sink': 0,
    'description': 'Where did it happened'
}

# Materialized fields

"""
For add/remove, the user supplies this info. For allocate/locate/receive, this info is
a readonly materialization of the the components of all the computers affected, to get an easier relationship
between component - event when the event is performed to a parent
"""
components = {
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
parent = {
    'type': 'string',
    'data_relation': {
        'resource': 'devices',
        'field': '_id',
        'embeddable': True
    },
    'description': 'The event triggered in this computer.'
}


class EventSettings(ResourceSettings):
    resource_methods = ['GET']
    _schema = Event  # We update the schema in DOMAIN
    datasource = {
        'source': 'events',
        'default_sort': [('_created', -1)]
    }
    mongo_indexes = {
        '@type': [('@type', pymongo.DESCENDING)],
        'device': [('device', pymongo.HASHED)],
        'components': [('components', pymongo.DESCENDING)],
    }
    cache_control = 'max-age=15, must-revalidate'


class EventSubSettings(EventSettings):
    _schema = False
    resource_methods = ['POST']
    item_methods = ['PATCH', 'DELETE']
    extra_response_fields = EXTRA_RESPONSE_FIELDS


class EventSubSettingsOneDevice(EventSubSettings):
    _schema = False


class EventSubSettingsMultipleDevices(EventSubSettings):
    _schema = False
