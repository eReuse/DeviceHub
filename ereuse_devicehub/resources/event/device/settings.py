from ereuse_devicehub.resources.event.settings import Event, EventSettings
from ereuse_devicehub.validation.coercer import Coercer

prefix = {'prefix': 'devices'}


class DeviceEvent(Event):
    geo = {
        'type': 'point',
        'sink': -5,
        'description': 'Where did it happened'
        # 'anyof': [{'required': True}, {'dependencies': ['place']}]  # me OR places
    }


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
        },
        'required': True
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
        'required': True
    }


EventWithDevices._settings = EventWithOneDevice._settings

place = {
    'type': 'objectid',  # It can optionally be the label of the place, be aware that place.label is not unique!
    'data_relation': {
        'resource': 'places',
        'field': '_id',
        'embeddable': True
    },
    'sink': 0,
    'coerce_with_context': Coercer.label_to_objectid,
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
    extra_response_fields = EventSettings.extra_response_fields + ['device', 'components']


class EventSubSettings(DeviceEventSettings):
    _schema = False
    resource_methods = ['POST']
    item_methods = ['GET', 'DELETE']


class EventSubSettingsOneDevice(EventSubSettings):
    _schema = False


class EventSubSettingsMultipleDevices(EventSubSettings):
    _schema = False
