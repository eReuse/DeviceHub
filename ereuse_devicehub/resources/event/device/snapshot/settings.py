import copy

from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.account.settings import unregistered_user, unregistered_user_doc
from ereuse_devicehub.resources.condition import condition
from ereuse_devicehub.resources.device.component.settings import Component
from ereuse_devicehub.resources.event.device.settings import place, EventWithOneDevice, EventSubSettingsOneDevice


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
        'allowed': ['DDI', 'Scan', 'DeviceHubClient'],
        'default': 'DDI'
    }
    events = {
        'type': 'list',  # Snapshot generates this automatically
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'events',
                'embeddable': True,
                'field': '_id'
            }
        },
        'readonly': True
    }
    request = {
        'type': 'string',  # The request sent, saved in case of debugging
        'readonly': True
    }
    unsecured = {
        'type': 'list',  # When we match an existing non-hid device, we state it here
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
        'readonly': True
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
        'doc': unregistered_user_doc
    }

    @classmethod
    def _clean(cls, attributes: dict, attributes_to_remove: tuple = None) -> dict:
        full_dict = super(Snapshot, cls)._clean(attributes, attributes_to_remove)
        full_dict['from'] = full_dict['_from']
        del full_dict['_from']
        return full_dict


class SnapshotSettings(EventSubSettingsOneDevice):
    _schema = Snapshot
    get_projection_blacklist = {Role.ADMIN: ('request',)}
    extra_response_fields = EventSubSettingsOneDevice.extra_response_fields + ['events']
    fa = 'fa-camera'
    short_description = "A fast picture of the state and key information of the computer and it's devices."
