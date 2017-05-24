from ereuse_devicehub.resources.group.settings import packages_fk, devices_fk, places_fk, lots_fk
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
            '_id': {
                'type': 'string'
            }
        }
    }


class UpdateGroupLogEntry(GroupLogEntry):
    """Saves the difference of the children of a group after every update."""
    added = {
        'type': 'dict',
        'schema': {
            'packages': packages_fk,
            'lots': lots_fk,
            'places': places_fk,
            'devices': devices_fk,
            'components': devices_fk
        }
    }
    removed = added


class GroupLogEntrySettings(ResourceSettings):
    _schema = GroupLogEntry
    url = 'groups/log'  # todo nice url: lots/xyz/log
    resource_methods = item_methods = ['GET']
    datasource = {
        'source': 'group-log-entry'
    }
