from ereuse_devicehub.resources.event.settings import Event, EventSettings

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
    'type': 'objectid',
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
    'description': 'Components affected by the event.'
}
parent = {
    'type': 'string',
    'data_relation': {
        'resource': 'devices',
        'field': '_id',
        'embeddable': True
    },
    'description': 'The event triggered in this computer.'
}


class DeviceEventSettings(EventSettings):
    _schema = DeviceEvent


class EventSubSettings(DeviceEventSettings):
    _schema = False
    resource_methods = ['POST']
    item_methods = ['GET']


class EventSubSettingsOneDevice(EventSubSettings):
    _schema = False


class EventSubSettingsMultipleDevices(EventSubSettings):
    _schema = False


