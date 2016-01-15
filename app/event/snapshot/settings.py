import copy

from app.account.user import Role
from app.device.component.settings import component
from app.device.computer.settings import computer
from app.event.settings import event_with_one_device, event_sub_settings_one_device

snapshot = copy.deepcopy(event_with_one_device)
snapshot.update({
    'offline': {
        'type': 'boolean'
    },
    'automatic': {
        'type': 'boolean'
    },
    'version': {
        'type': 'float',
    },
    'events': {
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
    },
    'request': {
        'type': 'string',  # The request sent, saved in case of debugging
        'readonly': True
    },
    'unsecured': {
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
                    'allowed': ('model', 'pid')
                }
            }
        },
        'default': [],
        'readonly': True
    },
    'device': {
        'type': 'dict',
        'schema': computer,
        'required': True
    },
    'components': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': component
        },
        'default': []
    },
    'debug': {
        'type': 'dict'
    }
})

# snapshot.update(register_account_schema) todo do the ability to do it when device it gets registered

snapshot_settings = copy.deepcopy(event_sub_settings_one_device)
snapshot_settings.update({
    'resource_methods': ['POST'],
    'schema': snapshot,
    'url': 'snapshot',
    'get_projection_blacklist': {Role.ADMIN: ('request',)},  # Just superusers
    'extra_response_fields': snapshot_settings['extra_response_fields'] + ['events', 'test_hard_drives']
})
snapshot_settings['datasource']['filter'] = {'@type': {'$eq': 'Snapshot'}}
