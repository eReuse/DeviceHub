import copy

from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.account.settings import unregistered_user
from ereuse_devicehub.resources.condition import condition
from ereuse_devicehub.resources.device.benchmark_settings import BenchmarkRamSysbench
from ereuse_devicehub.resources.device.component.settings import Component
from ereuse_devicehub.resources.event.device.settings import EventSubSettingsOneDevice, EventWithOneDevice, parent, \
    place
from ereuse_devicehub.resources.group.settings import Group
from ereuse_devicehub.resources.pricing import pricing


class Snapshot(EventWithOneDevice):
    _uuid = {
        'type': 'uuid',
        'unique': True,
        'teaser': False,
        'modifiable': False
        # todo require this in a month from jan 2016
    }
    offline = {
        'type': 'boolean'
    }
    automatic = {
        'type': 'boolean'
    }
    version = {
        'type': 'version',
        'teaser': False
    }
    snapshotSoftware = {
        'type': 'string',
        'allowed': {'Workbench', 'AndroidApp', 'Web', 'WorkbenchAuto', 'DesktopApp', 'Photobox'},
        'default': 'Workbench'
    }
    events = {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'events',
                'embeddable': True,
                'field': '_id'
            }
        },
        'readonly': True,
        'description': 'The events triggered by the Snapshot.'
    }
    request = {
        'type': 'string',
        'readonly': True,
        'doc': 'The whole Snapshot saved in case for debugging'
    }
    unsecured = {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                '_id': {
                    'type': 'string',
                    'data_relation': {
                        'resource': 'devices',
                        'field': '_id',
                        'embeddable': True
                    }
                },
                '@type': {
                    'type': 'string'
                },
                'type': {
                    'type': 'string',
                    'allowed': {'model', 'pid'}
                }
            }
        },
        'default': [],
        'readonly': True,
        'description': 'Information about existing non-HID device.'
    }
    device = {
        'type': 'dict',  # eve doesn't care about the type when GET values
        'required': True,
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        },
        'sink': 4
    }
    components = {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': Component,
            'data_relation': {
                'resource': 'devices',
                'field': '_id',
                'embeddable': True
            }
        },
        'default': [],
        'teaser': False
    }
    parent = parent
    debug = {
        'type': 'dict',
        'teaser': False
    }
    place = copy.deepcopy(place)
    place['description'] = 'Place the devices to an existing location.'
    place['label'] = 'Place where the devices are saved'
    software = {
        'type': 'dict',
        'schema': {
            'productKey': {
                'type': 'string'
            }
        },
        'sink': -1
    }
    condition = {
        'type': 'dict',
        'schema': condition,
        'sink': 1,
        'teaser': True
    }
    pricing = {
        'type': 'dict',
        'schema': pricing,
        'sink': 1,
        'teaser': True
    }
    _from = {
        'type': ['objectid', 'dict', 'string'],  # We should not add string but it does not work otherwise...
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True,
        },
        'get_from_data_relation_or_create': 'email',
        'schema': unregistered_user,
        'sink': 2,
        'label': 'E-mail of the giver',
        'description': 'The e-mail of the person or organization that gave the devices. You cannot change this later.',
        'doc': 'Disabled for now as incoming lot provides this functionality, want to see if it is really needed.',
        'readonly': True
    }
    elapsed = {
        'type': 'time'
    }
    osInstallation = {
        'type': 'dict',
        'schema': {
            'elapsed': {
                'type': 'time',
            },
            'label': {
                'type': 'string'
            },
            'success': {
                'type': 'boolean'
            }
        }
    }
    tests = {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'elapsed': {
                    'type': 'time'
                },
                'success': {
                    'type': 'boolean'
                },
                '@type': {
                    'type': 'string',
                    'allowed': ['StressTest']
                }
            }
        }
    }
    inventory = {
        'type': 'dict',
        'schema': {
            'elapsed': {
                'type': 'time'
            }
        }
    }
    date = {
        'type': 'datetime'
    }
    autoUploaded = {
        'type': 'boolean',
        'default': False
    }
    licenseKey = {
        'type': 'string'
    }
    group = {
        'type': 'dict',
        'schema': {
            '@type': {
                'type': 'string',
                'allowed': Group.types,
                'required': True
            },
            '_id': {
                'type': 'string',
                'required': True
            }
        },
        'description': 'Automatically add the device to the group, if any.',
        'doc': 'After performing the snapshot, adds the device to the group if it was not there already.'
    }
    color = {
        'type': 'string',
        'description': 'The primary color of the device.',
        'allowed_description': {
            '#000000': 'black',
            '#C0C0C0': 'silver',
            '#808080': 'gray',
            '#FFFFFF': 'white',
            '#800000': 'maroon',
            '#FF0000': 'red',
            '#800080': 'purple',
            '#FF00FF': 'fuchsia',
            '#008000': 'green',
            '#00FF00': 'lime',
            '#808000': 'olive',
            '#FFFF00': 'yellow',
            '#000080': 'navy',
            '#0000FF': 'blue',
            '#008080': 'teal',
            '#00FFFF': 'aqua'
        }
    }
    orientation = {
        'type': 'string',
        'allowed': {'Vertical', 'Horizontal'}
    }
    picture_info = {
        'type': 'dict',
        'schema': {
            'software': {
                'type': 'string',
                'allowed': {'Pbx'},
                'allowed_description': {
                    'Pbx': 'Photobox'
                },
                'description': 'The software used to take the picture.'
            },
            'version': {
                'type': 'version',
                'description': 'The version of the software.'
            }
        },
        'description': 'Information about the pictures of the device.'
    }
    pictures = {
        'type': 'list',
        'schema': {
            'type': 'media',
            'accept': 'image/jpeg'
        },
        'description': 'Pictures of the device.'
    }
    benchmarks = {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': BenchmarkRamSysbench
        }
    }

    @classmethod
    def _clean(cls, attributes: dict, attributes_to_remove: tuple = None) -> dict:
        full_dict = super(Snapshot, cls)._clean(attributes, attributes_to_remove)
        full_dict['from'] = full_dict.pop('_from')
        return full_dict


class SnapshotSettings(EventSubSettingsOneDevice):
    _schema = Snapshot
    get_projection_blacklist = {Role.ADMIN: ('request',)}
    extra_response_fields = EventSubSettingsOneDevice.extra_response_fields + ['events']
    fa = 'fa-camera'
    short_description = "A fast picture of the state and key information of the computer and it's devices."
