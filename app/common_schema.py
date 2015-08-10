__author__ = 'busta'


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
