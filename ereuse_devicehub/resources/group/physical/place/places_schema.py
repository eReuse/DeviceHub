from ereuse_devicehub.resources.schema import Thing


class SchemaPlace(Thing):
    pass


class City(SchemaPlace):
    confidence = {
        'type': 'natural'
    }


class Country(SchemaPlace):
    confidence = {
        'type': 'natural'
    }
    isoCode = {
        'type': 'string',
        'description': 'The ISO Code as ISO 3166-1'
    }


class AdministrativeArea(SchemaPlace):
    confidence = {
        'type': 'natural'
    }
    isoCode = {
        'type': 'string',
        'description': 'The ISO Code as ISO 3166-1'
    }


class Continent(SchemaPlace):
    geoipCode = {
        'type': 'string',
        'description': 'The GEOIP Code'
    }
