import copy

import pymongo

from app.schema import thing

place = copy.deepcopy(thing)
place.update({
    'geo': {
        'type': 'polygon',
        'sink': -5,
        'description': 'Set the area of the place. Be careful! Once set, you cannot update the area.',
        'modifiable': False
    },
    'type': {
        'type': 'string',
        'allowed': ['Department', 'Zone', 'Warehouse', 'CollectionPoint']
    },
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
        'default': [],
        'unique_values': True
    },
    'byUser': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True
        },
        'readonly': True
    }
})
place['label']['required'] = True
place['@type']['allowed'] = ['Place']

place_settings = {
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE', 'PUT'],
    'schema': place,
    'datasource': {
        'default_sort': [('_created', -1)]
    },
    'extra_response_fields': ['devices'],
    'url': 'places',
    'mongo_indexes': {
        'geo': [('components', pymongo.GEO2D)],
    }
}
