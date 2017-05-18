import copy
from collections import defaultdict

from ereuse_devicehub import utils
from ereuse_devicehub.resources.group.physical.settings import Physical, PhysicalSettings
from ereuse_devicehub.resources.group.settings import place_fk, packages_fk, lots_fk, devices_fk
from ereuse_devicehub.resources.schema import UnitCodes


def pallet_size():
    """Extracts and generates the size from the JSON `dimensions.json`."""
    file = utils.get_json_from_file('dimensions.json', same_directory_as_file=__file__)
    desc = defaultdict(dict)
    allowed = []
    factor = 1 / 25.4  # 1 in = 25.4 mm and we want otherwise
    for name, sizes in file.items():
        for width, depth in sizes:
            value = '{}-{}'.format(width, depth)
            allowed.append(value)
            t = '{} × {} mm – {} × {} in'.format(width, depth, round(width * factor, 2), round(depth * factor, 2))
            desc[name][value] = t
    return desc, allowed


_desc, _allowed = pallet_size()


class Pallet(Physical):
    weight = {
        'type': 'float',
        'unitCode': UnitCodes.kgm,
        'sink': -1,
        'teaser': False
    }
    size = {
        'type': 'string',
        'allowed': _allowed,
        'allowed_description': _desc
    }
    ancestors = copy.deepcopy(Physical.ancestors)
    ancestors['schema']['schema']['places'] = place_fk
    ancestors['schema']['schema']['lots'] = lots_fk
    children = copy.deepcopy(Physical.children)
    children['schema']['packages'] = packages_fk
    children['schema']['devices'] = devices_fk
    children['schema']['components'] = devices_fk


class PalletSettings(PhysicalSettings):
    resource_methods = ['GET', 'POST']
    item_methods = ['GET', 'PATCH', 'DELETE', 'PUT']
    _schema = Pallet
    datasource = {
        'default_sort': [('_modified', -1)],
        'source': 'pallets'
    }
    url = 'pallets'
    fa = 'fa-align-justify'
