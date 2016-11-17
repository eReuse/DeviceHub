import copy

from ereuse_devicehub.resources.account.settings import unregistered_user, unregistered_user_doc
from ereuse_devicehub.resources.event.device.settings import place, components, EventWithDevices, \
    EventSubSettingsMultipleDevices


class Receive(EventWithDevices):
    receiver = {
        'type': ['objectid', 'dict', 'string'],  # We should not add string but it does not work otherwise...
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True,
        },
        'schema': unregistered_user,
        'get_from_data_relation_or_create': 'email',
        'required': True,
        'sink': 2,
        'doc': 'The user that receives it. ' + unregistered_user_doc
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
    receiverOrganization = {
        'type': 'string',
        'readonly': True,
        'materialized': True,
        'doc': 'Materialization of the organization that, by the time of the receive, the user worked in.'
    }
    place = place
    components = copy.deepcopy(components)


Receive.components['readonly'] = True


# receive['@type'][OR] = 'employee', ('receiver', 'unregisteredReceiver.name')
# Receiver OR ReceiverEmail. We need to hook this in a required field so it is always executed
# And @type is an always required field so we can happily hook on it


class ReceiveSettings(EventSubSettingsMultipleDevices):
    _schema = Receive
    fa = 'fa-cart-arrow-down'
    sink = -7
    short_description = 'Someone receives the devices: you, a transporter, the client...'
