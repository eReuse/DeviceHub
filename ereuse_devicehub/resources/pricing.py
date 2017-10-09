_type = {
    'percentage': {
        'type': 'number',
        'min': 0,
        'max': 1
    },
    'amount': {
        'type': 'number',
        'min': 0,
        'max': 10000  # Sanity check
    }
}

_service = {
    'standard': {
        'type': 'dict',
        'schema': _type
    },
    'warranty2': {
        'type': 'dict',
        'schema': _type
    }
}

pricing = {
    'refurbisher': {
        'type': 'dict',
        'schema': _service
    },
    'retailer': {
        'type': 'dict',
        'schema': _service
    },
    'platform': {
        'type': 'dict',
        'schema': _service
    },
    'total': {
        'type': 'number',
        'min': 0,
        'max': 10000
    }
}
