from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.device.component.settings import Component
from ereuse_devicehub.resources.event.device.settings import place, EventWithOneDevice, EventSubSettingsOneDevice


class Snapshot(EventWithOneDevice):
    offline = {
        'type': 'boolean'
    }
    automatic = {
        'type': 'boolean'
    }
    version = {
        'type': 'version'
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
        'default': []
    }
    debug = {
        'type': 'dict'
    }
    place = place
    software = {
        'type': 'dict',
        'schema': {
            'productKey': {
                'type': 'string'
            }
        },
        'sink': -1
    }


class SnapshotSettings(EventSubSettingsOneDevice):
    _schema = Snapshot
    get_projection_blacklist = {Role.ADMIN: ('request',)}
    extra_response_fields = EventSubSettingsOneDevice.extra_response_fields + ['events']
    fa = 'fa-camera'
    short_description = "A fast picture of the state and key information of the computer and it's devices."
