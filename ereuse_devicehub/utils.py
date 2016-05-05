import json
import linecache
import sys

import inflection as inflection
from flask import Response, current_app
from flask.ext.cache import Cache
from werkzeug.local import LocalProxy

from ereuse_devicehub.exceptions import Redirect

cache = Cache(config={'CACHE_TYPE': 'simple'})


class Naming:
    """
        In DeviceHub there are many ways to name the same resource (yay!), this is because of all the different
        types of schemas we work in. But no worries, we offer easy ways to change between naming conventions.

        - TypeCase is the one represented with '@type' and follow PascalCase and always singular. This is the standard preferred one.
        - resource-case is the eve naming, using the standard URI conventions. This one is tricky, as although the types
        are represented in singular, the URI convention is to be plural (Event vs events), however just few of them
        follow this rule (Snapshot [type] to snapshot [resource]). You can set which ones you want to change their number.
        - python_case is the one used by python for its folders and modules. It is underscored and always singular.

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
        return inflection.underscore(inflection.singularize(string) if pluralize else string)

    @staticmethod
    def _standarize(string):
        value = inflection.dasherize(inflection.underscore(string))
        # We accept any text which my be in the singular or plural number
        from ereuse_devicehub.default_settings import RESOURCES_CHANGING_NUMBER  # todo use default
        resources_changing_number = RESOURCES_CHANGING_NUMBER
        pluralize = value in resources_changing_number or inflection.singularize(value) in resources_changing_number
        return inflection.pluralize(value) if pluralize else value, pluralize

    @staticmethod
    def type(string: str):
        _, pluralize = Naming._standarize(string)
        return inflection.camelize(inflection.singularize(string) if pluralize else string)

    @staticmethod
    def url_word(word: str):
        """
            Normalizes a full word to be inserted to an url. If the word has spaces, etc, is used '_' and not '-'
        """
        return inflection.parameterize(word, '_')


class NestedLookup:
    @staticmethod
    def __new__(cls, document, references, operation):
        """Lookup a key in a nested document, return a list of values
        From https://github.com/russellballestrini/nested-lookup/ but in python 3
        """
        return list(NestedLookup._nested_lookup(document, references, operation))

    @staticmethod
    def key_equality_factory(key_to_find):
        def key_equality(key, value):
            return key == key_to_find

        return key_equality

    @staticmethod
    def is_sub_type_factory(type):
        def _is_sub_type(key, value):
            return is_sub_type(value, type)

        return _is_sub_type

    @staticmethod
    def _nested_lookup(document, references, operation):
        """Lookup a key in a nested document, yield a value"""
        if isinstance(document, list):
            for d in document:
                for result in NestedLookup._nested_lookup(d, references, operation):
                    yield result

        if isinstance(document, dict):
            for k, v in document.items():
                if operation(k, v):
                    references.append((document, k))
                    yield v
                elif isinstance(v, dict):
                    for result in NestedLookup._nested_lookup(v, references, operation):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in NestedLookup._nested_lookup(d, references, operation):
                            yield result

def is_sub_type(value, type):
    try:
        return issubclass(value, type)
    except TypeError:
        return issubclass(value.__class__, type)

def get_last_exception_info():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


class GeneralHooks:
    @staticmethod
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

    @staticmethod
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
                    payload.cache_control.max_age = current_app.config['ITEM_CACHE']
            else:
                # If we are here it means it is an item endpoint, not a list (resource) endpoint
                payload.cache_control.max_age = current_app.config['ITEM_CACHE']
            payload.headers._list.append(get_header_link(resource_type))


def get_header_link(resource_type: str) -> ():
    return 'Link', '<http://www.ereuse.org/onthology/' + resource_type + '.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
