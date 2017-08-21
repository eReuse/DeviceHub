"""
We mimic https://schema.org/unitCode, in concrete
the UN/CEFACT Common Code.
"""
import copy
import functools
from collections import defaultdict

from passlib.utils import classproperty

from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.resource import Resource
from ereuse_devicehub.utils import Naming, NestedLookup


class UnitCodes:
    mbyte = '4L'
    mbps = 'E20'
    mhz = 'MHZ'
    gbyte = 'E34'
    ghz = 'A86'
    bit = 'A99'
    kgm = 'KGM'
    m = 'MTR'

    @classmethod
    def humanize(cls, code_to_search):
        for human_name, code in vars(cls).items():
            if code == code_to_search:
                return human_name

class RDFS(Resource):
    label = {
        'type': 'string',
        'sink': 5,
        'description': 'A short, descriptive title'
    }
    _type = {
        'type': 'string',
        'required': True,
        'teaser': False
    }
    _settings = {
        'prefix': None,
        """JSON-LD prefix to use in type. Override it to use prefix for the class."""
        'abstract': True,
        'attributes_to_remove': ('_settings', '_import_schemas', '_types',
                                 'type_name', 'types', 'resource_name', 'parent_type', 'resource_names')
    }
    _import_schemas = True
    created = {
        'type': 'datetime',
        'dh_allowed_write_roles': Role.SUPERUSER,
        'writeonly': True,
        'doc': 'Sets the _created and _updated, thought to be used in imports.'
    }

    @classmethod
    def actual_fields(cls):
        """
        Returns the fields of only this class.
        """
        fields = super(RDFS, cls).actual_fields()
        if cls._import_schemas:
            references = []
            NestedLookup(fields, references, NestedLookup.is_sub_type_factory(RDFS))
            for document, ref_key in references:
                document[ref_key] = document[ref_key]()
        return fields

    @staticmethod
    def __new__(cls, import_schemas=True) -> dict:
        """
            Returns all the attributes of all the heriarchy: sub-classess and super-classes.
        """
        RDFS._import_schemas = import_schemas  # todo not thread safe
        full_dict = cls.superclasses_fields(2)  # We ignore Object and Resource
        allowed = full_dict['@type']['allowed']
        full_dict.update(cls.subclasses_fields())
        full_dict['@type']['allowed'] |= allowed
        return full_dict

    @classmethod
    def subclasses_fields(cls):
        """
            Returns the attributes of the subclasses, except the actual one.

            This method automatically gathers and computes @type and type attributes. We remember that, for the @type
            and type of a superclass of n subclasses, they will both have all the 'allowed' attributes
            of the n subclasses.
        """
        fields = {}
        type_allowed = set()
        subtype_allowed = set()
        for subclass in cls.subclasses():
            subclass_fields = subclass.actual_fields()
            type_allowed |= subclass_fields.get('@type', {}).get('allowed', set())
            subtype_allowed |= set(subclass_fields.get('type', {}).get('allowed', set()))
            fields.update(subclass_fields)
        if '@type' in fields:
            fields['@type']['allowed'] |= type_allowed
        if 'type' in fields:
            fields['type']['allowed'] |= subtype_allowed
        return fields

    @classmethod
    def _clean(cls, attributes: dict, attributes_to_remove: tuple = None) -> dict:
        """
            Extends :func:`Resource._clean` by setting @type accordingly and adding the 'allowed' property.
        """
        attributes_to_remove = tuple() if attributes_to_remove is None else attributes_to_remove
        fields = super()._clean(attributes, attributes_to_remove + cls._settings['attributes_to_remove'])
        if '_type' in fields:
            fields['@type'] = fields['_type']
            del fields['_type']
            if 'allowed' not in fields['@type']:
                fields['@type']['allowed'] = {cls.type_name}
        else:
            fields['@type'] = copy.deepcopy(RDFS._type)
            fields['@type']['allowed'] = {cls.type_name}
        return fields

    @classproperty
    def resource_name(cls):
        return Naming.resource(cls.type_name)

    @classproperty
    def type_name(cls):
        return Naming.new_type(cls.__name__, cls._settings['prefix'])

    """The following methods are not used to build the schema"""

    @classproperty
    def types(cls):
        """
            Obtains the resource type (e.g. Accept) of the actual class and its subclasses.

            To use this method override before the attribute _settings['prefix'] and
            optionally override _settings['force_prefix'] which defaults at True.

            Read-only.
        """
        return {_class.type_name for _class in cls.subclasses() + [cls]}

    @classproperty
    def parent_type(cls):
        """Like types but only for direct children, not returning the parent."""
        return cls._parent().type_name

    @classproperty
    def resource_names(cls):
        return {Naming.resource(type_name) for type_name in cls.types}


class Thing(RDFS):
    url = {
        'type': 'url',
        'teaser': False,
        'doc': 'The url of the resource. If passed in, the value it is moved to sameAs.',
        'move': 'sameAs'
    }
    sameAs = {
        'type': 'list',
        'teaser': False,
        # 'readonly': True, todo should be readonly
        'unique': True,
    }
    description = {
        'type': 'string',
        'maxlength': 500,
        'sink': -4,
        'description': 'Full long description'
    }
