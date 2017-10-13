import copy

from ereuse_devicehub.resources.group.abstract.lot.policy import Policies
from ereuse_devicehub.resources.group.abstract.settings import Abstract, AbstractSettings
from ereuse_devicehub.resources.group.settings import devices_fk, lots_fk, packages_fk, pallets_fk, place_fk


class Lot(Abstract):
    policies = {
        'type': 'dict',
        'schema': Policies()
    }
    date = {
        'type': 'datetime',
        'sink': -2,
        'description': 'An agreed or official date of creation or transfer '
                       'for this lot, most useful in Incoming/Outgoing lots.'
    }
    label = copy.copy(Abstract.label)
    label['required'] = True
    ancestors = copy.deepcopy(Abstract.ancestors)
    ancestors['schema']['schema']['places'] = place_fk
    ancestors['schema']['schema']['lots'] = lots_fk
    children = copy.deepcopy(Abstract.children)
    children['schema']['packages'] = packages_fk
    children['schema']['pallets'] = pallets_fk
    children['schema']['lots'] = lots_fk
    children['schema']['devices'] = devices_fk
    children['schema']['components'] = devices_fk


class LotSettings(AbstractSettings):
    _schema = Lot
    datasource = {
        'default_sort': [('_modified', -1)],
        'source': 'lots'
    }
    fa = 'fa-folder'
    url = 'lots'
