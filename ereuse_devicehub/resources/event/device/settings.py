from ereuse_devicehub.resources.event.settings import Event, EventSettings
from ereuse_devicehub.validation.coercer import Coercer

prefix = {'prefix': 'devices'}


class DeviceEvent(Event):
    prefix = 'devices'

    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.geo = {
            'type': 'point',
            'sink': -5,
            'description': 'Where did it happened'
            # 'anyof': [{'required': True}, {'dependencies': ['place']}]  # me OR places
        }


class EventWithOneDevice(DeviceEvent):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.device = {
            'type': 'string',
            'data_relation': {
                'resource': 'devices',
                'field': '_id',
                'embeddable': True
            },
            'required': True
        }


class EventWithDevices(DeviceEvent):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.devices = {
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
    def config(self, parent=None):
        self.schema = DeviceEvent


class EventSubSettings(DeviceEventSettings):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.resource_methods = ['POST']
        self.item_methods = ['GET', 'DELETE']


class EventSubSettingsOneDevice(EventSubSettings):
    pass


class EventSubSettingsMultipleDevices(EventSubSettings):
    pass
