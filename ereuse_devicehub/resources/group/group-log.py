import copy

from ereuse_devicehub.resources.resource import ResourceSettings
from ereuse_devicehub.resources.schema import Thing


class GroupLogEntry(Thing):
    """
    A log entry to save when groups, devices and events are added/removed to/from other groups.

    Note that as per python-eve and MongoDB we have _created as the timestamp.
    """
    parent = {
        'type': 'dict',
        'schema': {
            '@type': {
                'type': 'string'
            },
            'key': {
                'type': 'string'
            }
        }
    }
    _type = copy.copy(Thing._type)
    _type['allowed'] = {'GroupLogEntryAdd', 'GroupLogEntryRemove'}


class GroupLogEntryDevice(GroupLogEntry):
    """An entry logging when a device was added/removed to a group."""
    device = {
        'type': 'string',
        'data_relation': {
            'resource': 'devices',
            'embeddable': True,
            'field': '_id'
        }
    }


class GroupLogSettings(ResourceSettings):
    _schema = GroupLogEntry
    resource_methods = ['GET']
    item_methods = ['GET', 'PATCH', 'DELETE', 'PUT']
    datasource = {
        'source': 'group-log'
    }


class DeviceGroupLogSettings(GroupLogSettings):
    _schema = GroupLogEntryDevice
    url = 'devices/<regex("([W])\w+"):device>/group-log'
