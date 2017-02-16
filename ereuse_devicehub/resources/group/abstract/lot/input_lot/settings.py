from ereuse_devicehub.resources.group.abstract.lot.settings import Lot, LotSettings


class InputLot(Lot):
    _from = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True
        },
        'sink': 2
    }
    fromOrganization = {
        # Materialization of the organization that  the user worked in
        'type': 'string',
        'readonly': True
    }


class InputLotSettings(LotSettings):
    _schema = InputLot
    url = None

