import linecache
import os
import sys

import inflection as inflection
from flask import json, Config
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})


class Naming:
    """
    In DeviceHub there are many ways to name the same resource (yay!), this is because of all the different
    types of schemas we work with. But no worries, we offer easy ways to change between naming conventions.

    - TypeCase (or resource-type) is the one represented with '@type' and follow PascalCase and always singular.
        This is the standard preferred one.
    - resource-case is the eve naming, using the standard URI conventions. This one is tricky, as although the types
        are represented in singular, the URI convention is to be plural (Event vs events), however just few of them
        follow this rule (Snapshot [type] to snapshot [resource]). You can set which ones you want to change their
        number.
    - python_case is the one used by python for its folders and modules. It is underscored and always singular.
    """
    TYPE_PREFIX = ':'
    RESOURCE_PREFIX = '_'

    @staticmethod
    def resource(string: str):
        """
            :param string: String can be type, resource or python case
        """
        try:
            prefix, resulting_type = Naming.pop_prefix(string)
            prefix += Naming.RESOURCE_PREFIX
        except IndexError:
            prefix = ''
            resulting_type = string
        resulting_type = inflection.dasherize(inflection.underscore(resulting_type))
        return prefix + (inflection.pluralize(resulting_type) if Naming._pluralize(resulting_type) else resulting_type)

    @staticmethod
    def python(string: str):
        """
            :param string: String can be type, resource or python case
        """
        return inflection.underscore(inflection.singularize(string) if Naming._pluralize(string) else string)

    @staticmethod
    def _pluralize(string: str):
        from ereuse_devicehub.default_settings import RESOURCES_CHANGING_NUMBER
        value = inflection.dasherize(inflection.underscore(string))
        return value in RESOURCES_CHANGING_NUMBER or inflection.singularize(value) in RESOURCES_CHANGING_NUMBER

    @staticmethod
    def type(string: str):
        try:
            prefix, resulting_type = Naming.pop_prefix(string)
            prefix += Naming.TYPE_PREFIX
        except IndexError:
            prefix = ''
            resulting_type = string
        resulting_type = inflection.singularize(resulting_type) if Naming._pluralize(resulting_type) else resulting_type
        resulting_type = resulting_type.replace('-', '_')  # camelize does not convert '-' but '_'
        return prefix + inflection.camelize(resulting_type)

    @staticmethod
    def url_word(word: str):
        """
            Normalizes a full word to be inserted to an url. If the word has spaces, etc, is used '_' and not '-'
        """
        return inflection.parameterize(word, '_')

    @staticmethod
    def pop_prefix(string: str):
        """Erases the prefix and returns it.
        :throws IndexError: There is no prefix.
        :return A set with two elements: 1- the prefix, 2- the type without it.
        """
        result = string.split(Naming.TYPE_PREFIX)
        if len(result) == 1:
            result = string.split(Naming.RESOURCE_PREFIX)
            if len(result) == 1:
                raise IndexError()
        return result

    @staticmethod
    def new_type(type_name: str, prefix: str or None = None) -> str:
        """
            Creates a resource type with optionally a prefix.

            Using the rules of JSON-LD, we use prefixes to disambiguate between different types with the same name:
            one can Accept a device or a project. In eReuse.org there are different events with the same names, in
            linked-data terms they have different URI. In eReuse.org, we solve this with the following:

                "@type": "devices:Accept" // the URI for these events is 'devices/events/accept'
                "@type": "projects:Accept"  // the URI for these events is 'projects/events/accept
                ...

            Type is only used in events, when there are ambiguities. The rest of

                "@type": "devices:Accept"
                "@type": "Accept"

            But these not:

                "@type": "projects:Accept"  // it is an event from a project
                "@type": "Accept"  // it is an event from a device
        """
        if Naming.TYPE_PREFIX in type_name:
            raise TypeError('Cannot create new type: type {} is already prefixed.'.format(type_name))
        prefix = (prefix + Naming.TYPE_PREFIX) if prefix is not None else ''
        return prefix + type_name


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


def is_sub_type(value, resource_type):
    try:
        return issubclass(value, resource_type)
    except TypeError:
        return issubclass(value.__class__, resource_type)


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
