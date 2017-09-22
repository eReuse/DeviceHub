import copy

from ereuse_devicehub.resources.event.settings import Event, EventSettings
from ereuse_devicehub.resources.group.settings import lots_fk, packages_fk
from ereuse_devicehub.security.perms import perms

prefix = {'prefix': 'devices'}


class DeviceEvent(Event):
    geo = {
        'type': 'point',
        'sink': -5,
        'description': 'Where did it happened'
        # 'anyof': [{'required': True}, {'dependencies': ['place']}]  # me OR places
    }
    perms = copy.copy(perms)
    # We always create this value through our hooks, but if set per 'default' for events
    # eve creates it in situations we don't want
    del perms['default']
    perms['materialized'] = True



settings = DeviceEvent._settings.copy()
settings.update({'url': 'devices'})
settings.update(prefix)
DeviceEvent._settings = settings  # todo make this nice


class EventWithOneDevice(DeviceEvent):
    device = {
        'type': 'string',
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        }
    }


EventWithOneDevice._settings = dict(Event._settings, **prefix)


class EventWithDevices(DeviceEvent):
    devices = {
        'type': 'list',
        'schema': {
            'type': 'string',
            'data_relation': {
                'resource': 'devices',
                'field': '_id',
                'embeddable': True
            }
        },
        'default': [],
        'doc': 'We want either \'devices\' xor \'groups\'.'
    }
    groups = {
        'type': 'dict',
        'schema': {
            'packages': packages_fk,
            'lots': lots_fk
        },
        'description': 'The groups the event has been performed on.',
        'doc': 'This field contains the groups and all its descendants.'
    }
    originalGroups = {
        'type': 'dict',
        'readonly': True,
        'schema': {
            'packages': packages_fk,
            'lots': lots_fk
        },
        'doc': 'The groups the user performed the event on, without its descendants.'
    }


EventWithDevices._settings = EventWithOneDevice._settings

place = {
    'type': 'string',  # It can optionally be the label of the place, be aware that place.label is not unique!
    'data_relation': {
        'resource': 'places',
        'field': '_id',
        'embeddable': True
    },
    'sink': 0,
    'description': 'Where did it happened'
}

# Materialized fields

"""
For add/remove, the user supplies this info. For allocate/locate/receive, this info is
a readonly materialization of the the components of all the computers affected, to get an easier relationship
between component - event when the event is performed to a parent
"""
components = {
    'type': 'list',
    'schema': {
        'type': 'string',
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        }
    },
    'description': 'Components affected by the event.',
    'teaser': False
}
materialized_components = copy.deepcopy(components)
materialized_components['materialized'] = True

parent_materialized = {
    'type': 'string',
    'data_relation': {
        'resource': 'devices',
        'field': '_id',
        'embeddable': True
    },
    'description': 'The event triggered in this computer.',
    'materialized': True
}

parent = {
    'type': 'string',
    'data_relation': {
        'resource': 'devices',
        'field': '_id',
        'embeddable': True
    },
    'doc': 'This is not the same as the materialized "parent" field. This field can be set when snapshotting a'
           ' component, for example through Scan, that should be included in a device.'
}


class DeviceEventSettings(EventSettings):
    _schema = DeviceEvent
    extra_response_fields = EventSettings.extra_response_fields + ['device', 'components', 'groups']


class EventSubSettings(DeviceEventSettings):
    _schema = False
    resource_methods = ['POST']
    item_methods = ['GET', 'DELETE']


class EventSubSettingsOneDevice(EventSubSettings):
    _schema = False


class EventSubSettingsMultipleDevices(EventSubSettings):
    _schema = False
