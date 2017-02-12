import copy

from ereuse_devicehub.resources.account.settings import unregistered_user, unregistered_user_doc
from ereuse_devicehub.resources.schema import Thing


class Policy(Thing):
    startDate = {
        'type': 'date'
    }
    endDate = {
        'type': 'date'
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
            'embeddable': True,
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
            'embeddable': True,
        },
        'schema': unregistered_user,
        'doc': 'A specific user where the devices have to go to' + unregistered_user_doc,
        'get_from_data_relation_or_create': 'email',
        'required': True,
        'sink': 2
    }


class Policies(Thing):
    dataDestruction = DataDestruction()
    authorizedResellers = AuthorizedResellers()
    authorizedRefubrishers = AuthorizedRefurbishers()
    authorizedReceivers = AuthorizedReceivers()
    finalDisposal = FinalDisposal()
    notifyPolicy = {
        'type': 'dict',
        'schema': {
            'disposal': NotifyPolicy(),
            'devicesSetToBeRepaired': NotifyPolicy(),
            'devicesSetToBeReused': NotifyPolicy(),
            'devicesSetToBeRecycled': NotifyPolicy(),
            'nonResponseOfReceiver': NotifyPolicy(),
            'refurbisherLocation': NotifyPolicy(),
            'refurbisherTipology': NotifyPolicy(),
            'startReuseTime': NotifyPolicy(),
            'endReuseTime': NotifyPolicy(),
            'deliveryNote': NotifyPolicy(),
            'receiver': NotifyPolicyWithUser(),
            'recycler': NotifyPolicyWithUser(),
            'reseller': NotifyPolicyWithUser(),
            'socialImpact': NotifyPolicy()
        }
    }
    description = copy.copy(Thing.description)
    description['description'] = 'Write here any custom policy or message you want other users to see.'
