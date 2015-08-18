__author__ = 'Xavier Bustamante Talavera'
from app.event.snapshot.settings import snapshot_settings


snapshot_file = {
    'file': {
        'type': 'string',
        'required': True
    }
}

snapshot_settings = {
    'resource_methods': ['POST'],
    'schema': snapshot_file,
    'datasource': {
        'source': 'events',
        'filter': {'@type': {'$eq': 'snapshot'}},
        'url': snapshot_settings['datasource']['url'] + '/file'
    }
}
