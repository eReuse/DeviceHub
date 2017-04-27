import pymongo

from ereuse_devicehub.resources.domain import Domain
from ereuse_devicehub.resources.resource import ResourceSettings
from ereuse_devicehub.resources.schema import Thing


class Organization(Thing):
    logo = {
        'type': 'url'
    }


class Manufacturer(Organization):
    pass


class ManufacturerSettings(ResourceSettings):
    _schema = Manufacturer
    resource_methods = ['GET']
    item_methods = ['GET']
    additional_lookup = {
        'url': 'regex("[w]+")',
        'field': 'label',
    }
    datasource = {
        'source': 'manufacturers',
        'default_sort': [('label', pymongo.ASCENDING)]
    }

    cache_control = 'max-age={}, public'.format(3 * 24 * 60 * 60)
    mongo_indexes = {
        'Man: label': [('label', pymongo.TEXT)]
    }
    use_default_database = True


class ManufacturerDomain(Domain):
    resource_settings = ManufacturerSettings
