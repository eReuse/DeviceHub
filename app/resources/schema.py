"""
We mimic https://schema.org/unitCode, in concrete
the UN/CEFACT Common Code.
"""
import copy


from app.resources.resource import Resource
from app.utils import Naming, nested_lookup, is_sub_type_factory


class UnitCodes:
    mbyte = '4L'
    mbps = 'E20'
    mhz = 'MHZ'
    gbyte = 'E34'
    ghz = 'A86'
    bit = 'A99'
    kgm = 'KGM'
    m = 'MTR'


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
        'abstract': True
    }

    @classmethod
    def actual_fields(cls):
        """
        Returns the fields of only this class.
        """
        fields = super(RDFS, cls).actual_fields()
        references = []
        nested_lookup(fields, references, is_sub_type_factory(RDFS))
        for document, ref_key in references:
            document[ref_key] = document[ref_key]()
        return fields

    @staticmethod
    def __new__(cls, *more) -> dict:
        """
            Returns all the attributes of all the heriarchy: sub-classess and super-classes.
        """
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
        fields = super()._clean(attributes, attributes_to_remove + ('_settings',))
        if '_type' in fields:
            fields['@type'] = fields['_type']
            del fields['_type']
            if 'allowed' not in fields['@type']:
                fields['@type']['allowed'] = {cls.__name__}
        else:
            fields['@type'] = copy.deepcopy(RDFS._type)
            fields['@type']['allowed'] = {cls.__name__}
        return fields

    @classmethod
    def resource_name(cls):
        return Naming.resource(cls.__name__)

    @classmethod
    def type_name(cls):
        return cls.__name__


class Thing(RDFS):
    url = {
        'type': 'url',
        'readonly': True,
        'teaser': False
    }
    sameAs = {
        'type': 'url',
        'teaser': False
    }
    description = {
        'type': 'string',
        'maxlength': 500,
        'sink': -4,
        'description': 'Full long description'
    }
