rdfs = {
    'label': {
        'type': 'string',
        'sink': 5,
        'description': 'A short, descriptive title'
    },
    '@type': {
        'type': 'string',
        'required': True
    }
}

thing = dict(rdfs, **{
    'url': {
        'type': 'url',
        'readonly': True
    },
    'sameAs': {
        'type': 'url'
    },
    'description': {
        'type': 'string',
        'maxlength': 500,
        'sink': -4,
        'description': 'Full long description'
    }
})
