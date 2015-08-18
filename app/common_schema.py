__author__ = 'Xavier Bustamante Talavera'


rdfs = {
    'label': {
        'type': 'string',
    },
    '@type': {
        'type': 'string'
    }
}

thing = dict({
    'url': {
        'type': 'string'
    },
    'sameAs': {
        'type': 'string'
    }
}, **rdfs)
