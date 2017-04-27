from ereuse_devicehub.resources.account.settings import unregistered_user
from ereuse_devicehub.resources.group.abstract.lot.settings import Lot, LotSettings


class IncomingLot(Lot):
    _from = {
        'type': ['objectid', 'dict', 'string'],  # We should not add string but it does not work otherwise...
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True
        },
        'sink': 2,
        'get_from_data_relation_or_create': 'email',
        'schema': unregistered_user,
    }
    fromOrganization = {
        # Materialization of the organization that  the user worked in
        'type': 'string',
        'readonly': True
    }

    @classmethod
    def _clean(cls, attributes: dict, attributes_to_remove: tuple = None) -> dict:
        full_dict = super(IncomingLot, cls)._clean(attributes, attributes_to_remove)
        full_dict['from'] = full_dict.pop('_from')
        return full_dict


class IncomingLotSettings(LotSettings):
    _schema = IncomingLot
    url = None
