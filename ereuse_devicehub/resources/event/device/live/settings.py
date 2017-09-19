from ereuse_devicehub.resources.event.device.settings import EventWithOneDevice, EventSubSettingsOneDevice, \
    materialized_components
from ereuse_devicehub.resources.group.physical.place.places_schema import Country, AdministrativeArea, Continent, City


class Live(EventWithOneDevice):
    ip = {
        'type': 'string',
        'readonly': True
    }
    country = {
        'type': 'dict',
        'schema': Country,
        'readonly': True
    }
    administrativeArea = {
        'type': 'dict',
        'schema': AdministrativeArea,
        'readonly': True
    }
    city = {
        'type': 'dict',
        'schema': City,
        'readonly': True
    }
    continent = {
        'type': 'dict',
        'schema': Continent,
        'readonly': True
    }
    isp = {
        'type': 'string',
        'readonly': True
    }
    organization = {
        'type': 'string',
        'readonly': True
    }
    userType = {
        'type': 'string',
        'readonly': True
    }
    autonomousSystemNumber = {
        'type': 'natural',
        'readonly': True
    }
    components = materialized_components


class LiveSettings(EventSubSettingsOneDevice):
    _schema = Live
