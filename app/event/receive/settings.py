import copy

from app.validation import OR
from app.event.settings import event_with_devices, event_sub_settings_multiple_devices

receive = copy.deepcopy(event_with_devices)
receive.update({
    'receiver': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True,
        },
    },
    'receiverEmail': {
        'type': 'string',
        'dependencies': ['receiverName']
    },
    'receiverName': {
        'type': 'string',
        'dependencies': ['receiverEmail']
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
})
receive['@type'][OR] = 'employee', ('receiver', 'receiverEmail')
# Receiver OR ReceiverEmail. We need to hook this in a required field so it is always executed
# And @type is an always required field so we can happily hook on it

receive_settings = copy.deepcopy(event_sub_settings_multiple_devices)
receive_settings.update({
    'schema': receive,
    'url': event_sub_settings_multiple_devices['url'] + 'receive'
})
receive_settings['datasource']['filter'] = {'@type': {'$eq': 'Receive'}}
