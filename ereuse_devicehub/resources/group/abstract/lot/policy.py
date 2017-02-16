import copy

from ereuse_devicehub.resources.account.settings import unregistered_user, unregistered_user_doc
from ereuse_devicehub.resources.schema import Thing


class Policy(Thing):
    startDate = {
        'type': 'datetime'
    }
    endDate = {
        'type': 'datetime'
    }

    _type = copy.copy(Thing.label)
    _type['allowed'] = {}


class DataCompliance(Policy):
    pass


class DataDestruction(DataCompliance):
    mechanical = {
        'type': 'boolean'
    }
    eraseBasic = {
        'type': 'boolean'
    }
    eraseSectors = {
        'type': 'boolean'
    }


class AuthorizedUsers(Policy):
    nonForProfit = {
        'type': 'boolean'
    }
    cooperative = {
        'type': 'boolean'
    }
    to = {
        'type': ['objectid', 'dict', 'string'],  # We should not add string but it does not work otherwise...
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True
        },
        'schema': unregistered_user,
        'doc': 'A specific user where the devices have to go to' + unregistered_user_doc,
        'get_from_data_relation_or_create': 'email',
        'required': True,
        'sink': 2
    }


class AuthorizedResellers(AuthorizedUsers):
    pass


class AuthorizedRefurbishers(AuthorizedUsers):
    pass


class AuthorizedReceivers(AuthorizedUsers):
    digitalGapIndividual = {
        'type': 'boolean'
    }


class FinalDisposal(Policy):
    returnToCircuit = {
        'type': 'boolean'
    }
    disposeToCollectionPoint = {
        'type': 'boolean'
    }
    returnToReseller = {
        'type': 'boolean'
    }


class NotifyPolicy(Policy):
    pass


class NotifyPolicyWithUser(NotifyPolicy):
    to = {
        'type': ['objectid', 'dict', 'string'],  # We should not add string but it does not work otherwise...
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True
        },
        'schema': unregistered_user,
        'doc': 'A specific user where the devices have to go to' + unregistered_user_doc,
        'get_from_data_relation_or_create': 'email',
        'required': True,
        'sink': 2
    }


class Policies(Thing):
    dataDestruction = {
        'type': 'dict',
        'schema': DataDestruction()
    }
    authorizedResellers = {
        'type': 'dict',
        'schema': AuthorizedResellers()
    }
    authorizedRefubrishers = {
        'type': 'dict',
        'schema': AuthorizedRefurbishers()
    }
    authorizedReceivers = {
        'type': 'dict',
        'schema': AuthorizedReceivers()
    }
    finalDisposal = {
        'type': 'dict',
        'schema': FinalDisposal()
    }
    notifyPolicy = {
        'type': 'dict',
        'schema': {
            'disposal': {'type': 'dict', 'schema': NotifyPolicy()},
            'devicesSetToBeRepaired': {'type': 'dict', 'schema': NotifyPolicy()},
            'devicesSetToBeReused': {'type': 'dict', 'schema': NotifyPolicy()},
            'devicesSetToBeRecycled': {'type': 'dict', 'schema': NotifyPolicy()},
            'nonResponseOfReceiver': {'type': 'dict', 'schema': NotifyPolicy()},
            'refurbisherLocation': {'type': 'dict', 'schema': NotifyPolicy()},
            'refurbisherTipology': {'type': 'dict', 'schema': NotifyPolicy()},
            'startReuseTime': {'type': 'dict', 'schema': NotifyPolicy()},
            'endReuseTime': {'type': 'dict', 'schema': NotifyPolicy()},
            'deliveryNote': {'type': 'dict', 'schema': NotifyPolicy()},
            'receiver': {'type': 'dict', 'schema': NotifyPolicyWithUser()},
            'recycler': {'type': 'dict', 'schema': NotifyPolicyWithUser()},
            'reseller': {'type': 'dict', 'schema': NotifyPolicyWithUser()},
            'socialImpact': {'type': 'dict', 'schema': NotifyPolicy()}
        }
    }
    description = copy.copy(Thing.description)
    description['description'] = 'Write here any custom policy or message you want other users to see.'
