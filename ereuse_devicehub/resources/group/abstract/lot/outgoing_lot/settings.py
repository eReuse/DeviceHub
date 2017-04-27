from ereuse_devicehub.resources.account.settings import unregistered_user, unregistered_user_doc
from ereuse_devicehub.resources.group.abstract.lot.settings import Lot, LotSettings


class OutgoingLot(Lot):
    to = {
        'type': ['objectid', 'dict', 'string'],  # We should not add string but it does not work otherwise...
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True
        },
        'schema': unregistered_user,
        'doc': 'The user the lot goes to ' + unregistered_user_doc,
        'get_from_data_relation_or_create': 'email',
        'sink': 2
    }
    toOrganization = {
        'type': 'string',
        'readonly': True,
        'materialized': True,
        'doc': 'Materialization of the organization that, by the time of the allocation, the user worked in.'
    }


class OutgoingLotSettings(LotSettings):
    _schema = OutgoingLot
    url = None  # todo we can get variables that do not go deep through __a convention
    pass
