import copy

from app.device.component.settings import component, component_sub_settings
from app.event.test_hard_drive.settings import test_hard_drive


def gen_list(x) -> list:
    return [x]

hard_drive = copy.deepcopy(component)
hard_drive_settings = copy.deepcopy(component_sub_settings)

hard_drive.update({
    'interface': {
        'type': 'string',
    },
    'size': {
        'type': 'float'  # In Megabytes
    },
    'erasures': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'erasureId': {'type': 'string', 'required': True},
                'timestamp': {'type': 'string', 'required': True},
                'cleanedSectors': {'type': 'string', 'required': True},
                'failedSectors': {'type': 'string', 'required': True},
                'totalSectors': {'type': 'string', 'required': True},
                'state': {'type': 'string', 'required': True},
                'elapsedTime': {'type': 'string', 'required': True},
                'startTime': {'type': 'string', 'required': True},
                'endTime': {'type': 'string', 'required': True},
                'erasureStandardName': {'type': 'string', 'required': True},
                'overwritingRounds': {'type': 'string', 'required': True},
                'firmwareRounds': {'type': 'string', 'required': True},
                'totalErasureRounds': {'type': 'string', 'required': True},
                'remappedSectors': {'type': 'string', 'required': True},
                'remappedSectorsAfterErasure': {'type': 'string', 'required': True},
                'health': {'type': 'string', 'required': True},
                'steps': {
                    'type': 'list',
                    'required': True,
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'number': {'type': 'string'},
                            'type': {'type': 'string'},
                            'pattern': {'type': 'string'},
                            'errors': {'type': 'string'},
                            'state': {'type': 'string'},
                            'elapsedTime': {'type': 'string'},
                            'startTime': {'type': 'string'},
                            'endTime': {'type': 'string'},
                            'processed': {
                                'type': 'dict',
                                'schema': {
                                    'type': {'type': 'string'},
                                    'nSectors': {'type': 'string'}
                                }
                            },
                            'regions': {
                                'type': 'list',
                                'schema': {
                                    'type': 'dict',
                                    'schema': {
                                        'type': {'type': 'string'},
                                        'capacity': {'type': 'string'},
                                        'sectors': {'type': 'string'},
                                        'status': {'type': 'string'}
                                    }
                                }
                            }
                        }
                    }
                },
            }
        }
    },
    'firmwareRevision': {
        'type': 'string'
    },
    'blockSize': {
        'type': 'integer',
    },
    'sectors': {
        'type': 'integer'
    },
    'test': {
        'type': ['dict'],
        'schema': copy.deepcopy(test_hard_drive),
    },
    'tests': {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'events',
                'field': '_id',
                'embeddable': True
            }
        },
        'readonly': True
    }
})
hard_drive['test']['schema']['device']['required'] = False
hard_drive_settings.update({
    'schema': hard_drive,
    'url': component_sub_settings['url'] + 'hard-drive',
    'etag_ignore_fields': hard_drive_settings['etag_ignore_fields'] + ['tests', 'erasures', 'test']
})

