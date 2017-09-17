from pymongo import ASCENDING

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
    """
    Manufacturers don't have pagination, so if we do GET /manufacturers we obtain *all* manufacturers. To fetch
    manufacturers in a typeahead we can still do GET /manufactures?max_results=6.
    
    Not having pagination enables to get all manufactures in a GET and speeds up eve, as it does not need to count
    totals nor pages.
    """
    _schema = Manufacturer
    resource_methods = ['GET']
    item_methods = ['GET']
    additional_lookup = {
        'url': 'regex("[w]+")',
        'field': 'label',
    }
    datasource = {
        'source': 'manufacturers',
        'default_sort': [('label', ASCENDING)]
    }
    pagination = False
    cache_control = 'max-age={}, public'.format(7 * 24 * 60 * 60)
    use_default_database = True


class ManufacturerDomain(Domain):
    resource_settings = ManufacturerSettings
