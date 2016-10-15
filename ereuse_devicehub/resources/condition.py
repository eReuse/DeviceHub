from ereuse_devicehub.validation.validation import DeviceHubValidator

"""Grades the state of the device in different areas."""
condition = {
    'appearance': {
        'type': 'dict',
        'schema': {
            'general': {
                'type': 'string',
                'allowed': DeviceHubValidator.SCALE_AD,
                'description': 'Grades the imperfections that aesthetically affect the device, but not its usage.'
            }
        }
    },
    'functionality': {
        'type': 'dict',
        'schema': {
            'general': {
                'type': 'string',
                'allowed': DeviceHubValidator.SCALE_AD,
                'description': 'Grades the defects of a device that affect its usage.'
            }
        }
    }
}
