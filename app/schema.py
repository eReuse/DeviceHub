__author__ = 'Xavier Bustamante Talavera'


rdfs = {
    'label': {
        'type': 'string',
    },
    '@type': {
        'type': 'string'
    }
}

thing = dict(rdfs, **{
    'url': {
        'type': 'string'
    },
    'sameAs': {
        'type': 'string'
    }
})
