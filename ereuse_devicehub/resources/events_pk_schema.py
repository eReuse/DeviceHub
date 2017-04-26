events = {
    'type': 'list',
    'schema': {
        'type': 'dict'
    },
    'materialized': True,
    'description': 'A list of events where the first one is the most recent.',
    'doc': 'Few values of events are kept, avoiding big documents. See device/hooks/MaterializeEvents.fields.'
}
