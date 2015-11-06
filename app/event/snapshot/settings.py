import copy

__author__ = 'Xavier Bustamante Talavera'
from app.event.settings import event_with_one_device, event_sub_settings_one_device
from app.device.computer.settings import computer

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
    'device': {
        'type': 'dict',
        'schema': computer
    },
    'components': {
        'type': 'list',
        'schema': {
            'type': 'dict',
        }
    }
})

snapshot_settings = copy.deepcopy(event_sub_settings_one_device)
snapshot_settings.update({
    'resource_methods': ['POST'],
    'schema': snapshot,
    'url': 'snapshot',
})
snapshot_settings['datasource']['filter'] = {'@type': {'$eq': 'Snapshot'}}
