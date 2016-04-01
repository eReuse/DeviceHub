import copy

from ereuse_devicehub.resources.event.settings import components, EventWithDevices, \
    EventSubSettingsMultipleDevices
from ereuse_devicehub.resources.account.settings import unregistered_user


class Allocate(EventWithDevices):
    to = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True,
        },
        'excludes': 'unregisteredTo',
        'or': ['unregisteredTo'],
        'sink': 2
    }
    unregisteredTo = {
        'type': 'dict',
        'schema': unregistered_user,
        'sink': 2
    }
    undefinedDate = {
        'type': 'boolean',
        'default': False,
        'excludes': 'date',
        'description': 'Check this to say: "This owner possessed the device for an undetermined amount of time".'
    }
    toOrganization = {  # Materialization of the organization that, by the time of the allocation, the user worked in
        'type': 'string',
        'readonly': True
    }
    components = copy.deepcopy(components)

Allocate.components['readonly'] = True


class AllocateSettings(EventSubSettingsMultipleDevices):
    _schema = Allocate

# Receiver OR ReceiverEmail. We need to hook this in a required field so it is always executed
# And @type is an always required field so we can happily hook on it

