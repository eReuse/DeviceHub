__author__ = 'Xavier Bustamante Talavera'


rdfs = {
    'label': {
        'type': 'string',
    },
    '@type': {
        'type': 'string',
        'required': True
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

