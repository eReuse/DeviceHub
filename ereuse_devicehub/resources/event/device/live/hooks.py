from contextlib import suppress

from flask import request, current_app
from geojson import Point
from inflection import camelize
from pydash import assign
from pydash import chain

GEONAMES = 'http://sws.geonames.org/{}'


def save_ip(prove_usages: list):
    for prove_usage in prove_usages:
        if 'REVERSE_PROXY_REQUEST_HEADER' in current_app.config:
            ip = request.environ[current_app.config['REVERSE_PROXY_REQUEST_HEADER']]
        else:
            ip = request.remote_addr
        response = current_app.geoip(ip)  # Let's just get the dict
        prove_usage['ip'] = ip
        # regular values
        PICK = ('isp', 'organization', 'user_type', 'autonomous_system_number')
        traits = response.raw['traits']
        values = chain(traits).deep_pick(*PICK, discard_falsey=True).map_keys(lambda _, x: camelize(x, False)).value()
        assign(prove_usage, values)
        with suppress(AttributeError):
            prove_usage['city'] = {
                '@type': 'City',
                'confidence': response.city.confidence,
                'sameAs': GEONAMES.format(response.city.geoname_id),
                'name': response.city.name
            }
        with suppress(AttributeError):
            prove_usage['continent'] = {
                '@type': 'Continent',
                'sameAs': GEONAMES.format(response.continent.geoname_id),
                'geoipCode': response.continent.code,
                'name': response.continent.name
            }
        with suppress(AttributeError):
            prove_usage['country'] = {
                '@type': 'Country',
                'sameAs': GEONAMES.format(response.country.geoname_id),
                'isoCode': response.country.iso_code,
                'name': response.country.name,
                'confidence': response.country.confidence
            }
        with suppress(AttributeError):
            prove_usage['geo'] = Point((response.location.longitude, response.location.latitude))
            prove_usage['geo']['accuracy'] = response.location.accuracy_radius
        with suppress(IndexError, AttributeError):
            subdivision = response.subdivisions[-1]
            prove_usage['administrativeArea'] = {
                '@type': 'AdministrativeArea',
                'sameAs': GEONAMES.format(subdivision.geoname_id),
                'confidence': subdivision.confidence,
                'isoCode': subdivision.iso_code,
                'name': subdivision.name
            }
