import linecache
import os
import sys

from bson import ObjectId
from ereuse_utils.nested_lookup import NestedLookup
from flask import Config, json
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})


def get_last_exception_info():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


def coerce_type(fields: dict):
    """
    Similar to a Cerberus' coercion, adds a prefix to all @types accordingly.
    :param fields: the resource (ex-JSON document) to coerce. The variable is updated.
    """
    # todo this method should be general: obtaining which resources need to be prefixed from their schema
    from ereuse_devicehub.resources.event.device import DeviceEventDomain
    references = []
    NestedLookup(fields, references, NestedLookup.key_equality_factory('@type'))
    for document, ref_key in references:
        document[ref_key] = DeviceEventDomain.add_prefix(document[ref_key])


def get_header_link(resource_type: str) -> ():
    return 'Link', '<http://www.ereuse.org/onthology/' + resource_type + \
           '.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'


def get_json_from_file(filename: str, directory: str = None, parse_json=True, mode='r',
                       same_directory_as_file: str = None) -> dict:
    """

    :param parse_json: Try to parse the json or only return the string?
    :param mode: File opening mode. By default only read.
    :type filename: str
    :param directory: Optional. Directory to get the file from. If nothing, it is taken from .
    :param same_directory_as_file: Optional. If supplied, directory is set to the same directory as the file, overriding
    param *directory*.
    :return: JSON dict
    """
    if same_directory_as_file:
        directory = os.path.dirname(os.path.realpath(same_directory_as_file))
    with open(os.path.abspath(os.path.join(directory, filename)), mode=mode) as data_file:
        value = json.load(data_file) if parse_json else data_file.read()
    return value


class DeviceHubConfig(Config):
    """Configuration class for DeviceHub. We only extend it to add our settings when eve loads its settings."""

    def from_object(self, obj):
        super().from_object(obj)  # 1. Load settings as normal
        if obj == 'eve.default_settings':
            super().from_object('ereuse_devicehub.default_settings')  # 2. If those were eve's, then load ours


def url_for_resource(resource_name: str, _id: str or ObjectId, db: str = None, base_url: str = None) -> str:
    """Url for a resource"""
    from ereuse_devicehub.resources.account.domain import AccountDomain
    from flask import current_app
    db = db or AccountDomain.requested_database
    base_url = base_url or current_app.config['BASE_URL_FOR_AGENTS']
    return '{}/{}/{}/{}'.format(base_url, db, current_app.config['DOMAIN'][resource_name]['url'], _id)
