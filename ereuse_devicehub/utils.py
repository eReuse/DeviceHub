import linecache
import sys

import inflection as inflection
from flask.ext.cache import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})


class Naming:
    TYPE_PREFIX = ':'
    RESOURCE_PREFIX = '_'

    """
        In DeviceHub there are many ways to name the same resource (yay!), this is because of all the different
        types of schemas we work in. But no worries, we offer easy ways to change between naming conventions.

        - TypeCase (or resource-type) is the one represented with '@type' and follow PascalCase and always singular. This is the standard preferred one.
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
        try:
            prefix, string = Naming.pop_prefix(string)
            prefix += Naming.RESOURCE_PREFIX
        except IndexError:
            prefix = ''
        value = inflection.dasherize(inflection.underscore(string))
        # We accept any text which my be in the singular or plural number

        from ereuse_devicehub.default_settings import RESOURCES_CHANGING_NUMBER  # todo use default
        resources_changing_number = RESOURCES_CHANGING_NUMBER
        pluralize = value in resources_changing_number or inflection.singularize(value) in resources_changing_number
        return prefix + (inflection.pluralize(value) if pluralize else value), pluralize

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

    @staticmethod
    def pop_prefix(string: str):
        """Erases the prefix and returns it.
        :throws IndexError: There is no prefix.
        :return A set with two elements: 1- the prefix, 2- the type without it.
        """
        if ':' not in string:
            raise IndexError()
        return string.split(Naming.TYPE_PREFIX)

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
        prefix = (prefix + ':') if prefix is not None else ''
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
    return 'Link', '<http://www.ereuse.org/onthology/' + resource_type + '.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'


class ClassProperty(property):
    """Defines *getting* properties from classes in python, from http://stackoverflow.com/a/29994957/2710757"""

    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()
