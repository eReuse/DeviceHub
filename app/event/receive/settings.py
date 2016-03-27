import copy

from app.account.settings import unregistered_user
from app.event.settings import event_with_devices, event_sub_settings_multiple_devices, place, components

receive = copy.deepcopy(event_with_devices)
receive.update({
    'receiver': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True,
        },
        'excludes': 'unregisteredReceiver',
        'or': ['unregisteredReceiver'],
        'sink': 2
    },
    'unregisteredReceiver': {
        'type': 'dict',
        'schema': unregistered_user,
        'sink': 2
    },
    'acceptedConditions': {
        'type': 'boolean',
        'required': True,
        'allowed': [True]
    },
    'type': {
        'type': 'string',
        'required': True,
        'allowed': ['FinalUser', 'CollectionPoint', 'RecyclingPoint']
    },
    'automaticallyAllocate': {
        'type': 'boolean',
        'default': False,
        'description': 'Allocates to the user'
    },
    'receiverOrganization': {  # Materialization of the organization that, by the time of the receive, the user worked in
        'type': 'string',
        'readonly': True
    }
})
receive.update(copy.deepcopy(place))
receive.update(copy.deepcopy(components))
receive['components']['readonly'] = True
#receive['@type'][OR] = 'employee', ('receiver', 'unregisteredReceiver.name')
# Receiver OR ReceiverEmail. We need to hook this in a required field so it is always executed
# And @type is an always required field so we can happily hook on it

receive_settings = copy.deepcopy(event_sub_settings_multiple_devices)
receive_settings.update({
    'schema': receive
})
