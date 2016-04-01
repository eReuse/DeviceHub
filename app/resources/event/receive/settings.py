import copy

from app.resources.event.settings import place, components, EventWithDevices, \
    EventSubSettingsMultipleDevices
from app.resources.account.settings import unregistered_user


class Receive(EventWithDevices):
    receiver = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True,
        },
        'excludes': 'unregisteredReceiver',
        'or': ['unregisteredReceiver'],
        'sink': 2
    }
    unregisteredReceiver = {
        'type': 'dict',
        'schema': unregistered_user,
        'sink': 2
    }
    acceptedConditions = {
        'type': 'boolean',
        'required': True,
        'allowed': {True}
    }
    type = {
        'type': 'string',
        'required': True,
        'allowed': {'FinalUser', 'CollectionPoint', 'RecyclingPoint'}
    }
    automaticallyAllocate = {
        'type': 'boolean',
        'default': False,
        'description': 'Allocates to the user'
    }
    receiverOrganization = {  # Materialization of the organization that, by the time of the receive, the user worked in
        'type': 'string',
        'readonly': True
    }
    place = place
    components = copy.deepcopy(components)
Receive.components['readonly'] = True


# receive['@type'][OR] = 'employee', ('receiver', 'unregisteredReceiver.name')
# Receiver OR ReceiverEmail. We need to hook this in a required field so it is always executed
# And @type is an always required field so we can happily hook on it


class ReceiveSettings(EventSubSettingsMultipleDevices):
    _schema = Receive
