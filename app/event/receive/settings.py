import copy

from app.account.settings import unregistered_user
from app.event.settings import event_with_devices, event_sub_settings_multiple_devices, place

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
    'transferProperty': {
        'type': 'boolean',
        'default': False
    }
})
receive.update(copy.deepcopy(place))
#receive['@type'][OR] = 'employee', ('receiver', 'unregisteredReceiver.name')
# Receiver OR ReceiverEmail. We need to hook this in a required field so it is always executed
# And @type is an always required field so we can happily hook on it

receive_settings = copy.deepcopy(event_sub_settings_multiple_devices)
receive_settings.update({
    'schema': receive,
    'url': event_sub_settings_multiple_devices['url'] + 'receive'
})
receive_settings['datasource']['filter'] = {'@type': {'$eq': 'Receive'}}
