step = {
    '@type': {
        'type': 'string',
        'allowed': ['Zeros', 'Random'],
        'required': True
    },
    'success': {
        'type': 'boolean',
        'required': True
    },
    'startingTime': {
        'type': 'datetime'
    },
    'endingTime': {
        'type': 'datetime'
    },
    'secureRandomSteps': {
        'type': 'boolean'
    },
    'cleanWithZeros': {
        'type': 'boolean'
    }
}
