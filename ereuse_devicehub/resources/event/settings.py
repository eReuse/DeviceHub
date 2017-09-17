from ereuse_devicehub.resources.resource import ResourceSettings
from ereuse_devicehub.resources.schema import Thing
from ereuse_devicehub.validation.coercer import Coercer


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
    byUser = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True
        },
        'sink': 2,
        'coerce_with_context': Coercer.url_to_id
    }
    byOrganization = {  # Materialization of the organization that, by the time of the event, the user worked in
        'type': 'string',
        'readonly': True
    }


class EventSettings(ResourceSettings):
    resource_methods = ['GET']
    item_methods = ['GET', 'DELETE']
    _schema = Event  # We update the schema in DOMAIN
    datasource = {
        'source': 'events',
        'default_sort': [('_created', -1)]
    }
    cache_control = 'max-age=15, must-revalidate'
    fa = 'fa-bookmark-o'
