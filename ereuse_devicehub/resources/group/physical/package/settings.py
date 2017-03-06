import copy

from ereuse_devicehub.resources.group.physical.settings import Physical, PhysicalSettings
from ereuse_devicehub.resources.group.settings import place_fk, packages_fk, lots_fk, \
    devices_fk
from ereuse_devicehub.resources.schema import UnitCodes


class Package(Physical):
    weight = {
        'type': 'float',
        'unitCode': UnitCodes.kgm,
        'sink': -1,
        'teaser': False
    }
    width = {
        'type': 'float',
        'unitCode': UnitCodes.m,
        'sink': -1,
        'teaser': False
    }
    height = {
        'type': 'float',
        'unitCode': UnitCodes.m,
        'sink': -1,
        'teaser': False
    }
    depth = {
        'type': 'float',
        'unitCode': UnitCodes.m,
        'sink': -1,
        'teaser': False
    }
    ancestors = copy.deepcopy(Physical.ancestors)
    ancestors['schema']['schema']['places'] = place_fk
    ancestors['schema']['schema']['lots'] = lots_fk
    ancestors['schema']['schema']['packages'] = packages_fk
    children = copy.deepcopy(Physical.children)
    children['schema']['packages'] = packages_fk
    children['schema']['lots'] = lots_fk
    children['schema']['devices'] = devices_fk
    children['schema']['components'] = devices_fk


class PackageSettings(PhysicalSettings):
    resource_methods = ['GET', 'POST']
    item_methods = ['GET', 'PATCH', 'DELETE', 'PUT']
    _schema = Package
    datasource = {
        'default_sort': [('_modified', -1)],
        'source': 'packages'
    }
    url = 'packages'
    fa = 'fa-archive'
