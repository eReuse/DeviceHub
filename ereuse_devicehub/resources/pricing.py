_service = {
    'standard': {
        'type': 'dict',
        'schema': {
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
    }
}
