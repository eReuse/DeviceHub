
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
    }
}
