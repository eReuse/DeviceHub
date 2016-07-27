import copy

import iso3166
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
    address = {
        'type': 'dict',
        'schema': {
            'addressCountry': {
                'type': 'string',
                'allowed': {key for key in iso3166.countries_by_alpha2},
                'description': 'The name of the country',
                'doc': 'The addressCountry as per ISO 3166 (2 characters).'
            },
            'addressLocality': {
                'type': 'string',
                'description': 'The locality. For example, Barcelona.'
            },
            'addressRegion': {
                'type': 'string',
                'description': 'The region. For example, CA.'
            },
            'postalCode': {
                'type': 'string',
                'description': 'The postal code. For example, 94043.'
            },
            'streetAddress': {
                'type': 'string',
                'description': 'The street address. For example, C/Jordi Girona, 1-3.'
            }
        }
    }
    telephone = {
        'type': 'string'
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
