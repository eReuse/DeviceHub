import copy
import json
import linecache
import sys
from importlib import import_module

import inflection as inflection
from flask import Response
from werkzeug.local import LocalProxy

from app.exceptions import Redirect


class Naming:
    """
        In DeviceHub there are many ways to name the same resource (yay!), this is because of all the different
        types of schemas we work in. But no worries, we offer easy ways to change between naming conventions.

        - TypeCase is the one represented with '@type' and follow PascalCase and always singular. This is the standard preferred one.
        - resource-case is the eve naming, using the standard URI conventions. This one is tricky, as although the types
        are represented in singular, the URI convention is to be plural (Event vs events), however just few of them
        follow this rule (Snapshot [type] to snapshot [resource]). You can set which ones you want to change their number.
        - python_case is the one used by python for its folders and modules. It is underscored and always singular
    """
    @staticmethod
    def resource(string: str):
        """
            :param string: String can be type, resource or python case
        """
        return Naming._standarize(string)[0]

    @staticmethod
    def python(string: str):
        """
            :param string: String can be type, resource or python case
        """
        _, pluralize = Naming._standarize(string)
        a = inflection.underscore(inflection.singularize(string) if pluralize else string)
        return a

    @staticmethod
    def _standarize(string):
        from app.settings import RESOURCES_CHANGING_NUMBER
        value = inflection.dasherize(inflection.underscore(string))
        # We accept any text which my be in the singular or plural number
        pluralize = value in RESOURCES_CHANGING_NUMBER or inflection.singularize(value) in RESOURCES_CHANGING_NUMBER
        return inflection.pluralize(value) if pluralize else value, pluralize


def register_sub_types(domain: dict, parent_type: str, types_to_register=()) -> dict:
    """
    Given the following folder structure:
    parent_type/
                /subtype1
                /subtype2
                /...
    Where each subtype folder has a 'settings.py' file with a {subtype}_settings dictionary,
    it updates domain dict by adding a new key (subtype name) and {subtype}_settings dictionary.
    Ultimately, returns a full schema, resulting of merging all schemas found in {subtype}_settings
    dictionary.
    :param domain: dict to update.
    :param parent_type:
    :param types_to_register:
    :return: A newly deeped copied schema
    """
    merged_schema = {'@type': {'allowed': []}}
    for type_c in types_to_register:
        type_u = inflection.underscore(type_c)
        settings = import_module('.' + type_u + '.settings', parent_type)
        type_definition = getattr(settings, type_u + '_settings')
        register_sub_type(type_definition, domain, merged_schema, type_c)
    return copy.deepcopy(merged_schema)  # We copy it so we avoid others to work with references


def import_submodules(package_name):
    """ Import all submodules of a module, recursively

    :param package_name: Package name
    :type package_name: str
    :rtype: dict[types.ModuleType]
    """
    package = sys.modules[package_name]
    return {
        name: importlib.import_module(package_name + '.' + name)
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__)
    }

def register_sub_type(type_settings: dict, domain: dict, merged_schema: dict, type_c: str):
    """
    Register one sub type, take a look at 'register_sub_types' to get more info
    :param type_settings: The resource settings dictionary
    :param domain: Eve's site domain dictionary
    :param merged_schema: The result dictionary of inserting all the schemas, normally used for the generic event
    Merged schema needs to have '@type' and inside it 'allowed', being a list
    :param type_c: PascalCase type name
    """
    type_settings['schema']['@type']['allowed'] = [type_c]
    domain.update({Naming.resource(type_c): type_settings})
    new_type_settings_schema = copy.deepcopy(type_settings['schema'])
    del new_type_settings_schema['@type']  # We do not want to override 'allowed' in @type with the sub_type
    merged_schema.update(new_type_settings_schema)
    merged_schema['@type']['allowed'].append(type_c)


def difference(new_list: list, old_list: list) -> list:
    """
    Computes the difference between two lists of values
    :param new_list: List which we want the values from
    :param old_list: List to check against
    :return:
    """
    diff = []
    for x in new_list:
        found = False
        for y in old_list:
            if x == y:
                found = True
        if not found:
            diff.append(x)
    return diff


def set_response_headers_and_cache(resource: str, request: LocalProxy, payload: Response):
    """
    Sets JSON Header link referring to @type
    """
    if (payload._status_code == 200 or payload._status_code == 304) and resource is not None:
        data = json.loads(payload.data.decode(payload.charset))
        resource_type = resource
        try:
            resource_type = data['@type']
        except KeyError:
            if payload._status_code == 304:
                payload.cache_control.max_age = 120
        else:
            # If we are here it means it is an item endpoint, not a list (resource) endpoint
            payload.cache_control.max_age = 120
        payload.headers._list.append(get_header_link(resource_type))


def get_header_link(resource_type: str) -> ():
    return 'Link', '<http://www.ereuse.org/onthology/' + resource_type + '.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'


def normalize(string):
    return inflection.parameterize(string, '_')


def nested_lookup(key, document):
    """Lookup a key in a nested document, return a list of values
    From https://github.com/russellballestrini/nested-lookup/ but in python 3
    """
    return list(_nested_lookup(key, document))


def _nested_lookup(key, document):
    """Lookup a key in a nested document, yield a value"""
    if isinstance(document, list):
        for d in document:
            for result in _nested_lookup(key, d):
                yield result

    if isinstance(document, dict):
        for k, v in document.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in _nested_lookup(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in _nested_lookup(key, d):
                        yield result


def get_last_exception_info():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


def redirect_on_browser(resource, request, lookup):
    """
    Redirects the browsers to the client webApp.
    :param resource:
    :param request:
    :param lookup:
    :return:
    """
    if request.accept_mimetypes.accept_html:
        raise Redirect()
