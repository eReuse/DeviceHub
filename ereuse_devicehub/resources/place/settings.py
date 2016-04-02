import copy

import pymongo

from ereuse_devicehub.resources.resource import ResourceSettings
from ereuse_devicehub.resources.schema import Thing


class Place(Thing):
    geo = {
        'type': 'polygon',
        'sink': -5,
        'description': 'Set the area of the place. Be careful! Once set, you cannot update the area.',
        'modifiable': False
    }
    type = {
        'type': 'string',
        'allowed': {'Department', 'Zone', 'Warehouse', 'CollectionPoint'}
    }
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
        'default': [],
        'unique_values': True
    }
    byUser = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True
        },
        'readonly': True
    }
    label = copy.deepcopy(Thing.label)


Place.label['required'] = True


class PlaceSettings(ResourceSettings):
    resource_methods = ['GET', 'POST']
    item_methods = ['GET', 'PATCH', 'DELETE', 'PUT']
    _schema = Place
    datasource = {
        'default_sort': [('_created', -1)],
        'source': 'places'
    }
    extra_response_fields = ResourceSettings.extra_response_fields + ['devices']
    mongo_indexes = {
        'geo': [('components', pymongo.GEO2D)]
    }
