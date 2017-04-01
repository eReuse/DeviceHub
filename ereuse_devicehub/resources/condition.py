from ereuse_devicehub.validation.validation import DeviceHubValidator

"""Grades the state of the device in different areas."""
condition = {
    'appearance': {
        'type': 'dict',
        'schema': {
            'general': {
                'type': 'string',
                'allowed': DeviceHubValidator.SCALE_0E,
                'allowed_description': {
                    '0': '0. The device is new',
                    'A': 'A. Is like new (without visual damage)',
                    'B': 'B. Is in really good condition (small visual damage in difficult places to spot)',
                    'C': 'C. Is in good condition (small visual damage in parts that are easy to spot, not on screens)',
                    'D': 'D. Is acceptable (visual damage in visible parts, not on screens)',
                    'E': 'E. Is unacceptable (considerable visual damage that can affect usage)'
                },
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
                'allowed_description': {
                    'A': 'A. Everything works perfectly (buttons, and in case of screens there are no scratches)',
                    'B': 'B. There is a button difficult to press or a small scratch in an edge of a screen',
                    'C': 'C. A non-important button (or similar) doesn\'t work; screen has multiple scratches in edges',
                    'D': 'D. Multiple buttons don\'t work; screen has visual damage resulting in uncomfortable usage',
                },
                'description': 'Grades the defects of a device that affect its usage.',
            }
        }
    },
    'labelling': {
        'type': 'boolean',
        'default': False,
        'description': 'Sets if there are labels stuck that should be removed.'
    },
    'bios': {
        'type': 'dict',
        'schema': {
            'general': {
                'type': 'string',
                'allowed': DeviceHubValidator.SCALE_AE,
                'allowed_description': {
                    'A': 'A. If by pressing a key you could access a boot menu with the network boot',
                    'B': 'B. You had to get into the BIOS, and in less than 5 steps you could set the network boot',
                    'C': 'C. Like B, but with more than 5 steps',
                    'D': 'D. Like B or C, but you had to unlock the BIOS (i.e. by removing the battery)',
                    'E': 'E. The device could not be booted through the network.'
                },
                'description': 'How difficult it has been to set the bios to boot from the network.'
            }
        }
    }
}
