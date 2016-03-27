import copy

from app.account.settings import unregistered_user
from app.event.settings import event_with_devices, event_sub_settings_multiple_devices, components

allocate = copy.deepcopy(event_with_devices)
allocate.update({
    'to': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True,
        },
        'excludes': 'unregisteredTo',
        'or': ['unregisteredTo'],
        'sink': 2
    },
    'unregisteredTo': {
        'type': 'dict',
        'schema': unregistered_user,
        'sink': 2
    },
    'undefinedDate': {
        'type': 'boolean',
        'default': False,
        'excludes': 'date',
        'description': 'Check this to say: "This owner possessed the device for an undetermined amount of time".'
    },
    'toOrganization': {  # Materialization of the organization that, by the time of the allocation, the user worked in
        'type': 'string',
        'readonly': True
    }
})
allocate.update(copy.deepcopy(components))
allocate['components']['readonly'] = True

# Receiver OR ReceiverEmail. We need to hook this in a required field so it is always executed
# And @type is an always required field so we can happily hook on it

allocate_settings = copy.deepcopy(event_sub_settings_multiple_devices)
allocate_settings.update({
    'schema': allocate
})
