import copy

from ereuse_devicehub.resources.group.abstract.lot.policy import Policies
from ereuse_devicehub.resources.group.abstract.settings import AbstractSettings, Abstract
from ereuse_devicehub.resources.group.settings import place_fk, packages_fk, places_fk, lots_fk, \
    devices_fk, pallets_fk


class Lot(Abstract):
    policies = {
        'type': 'dict',
        'schema': Policies()
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
    fa = 'fa-cubes'
    url = 'lots'
