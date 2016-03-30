"""
We mimic https://schema.org/unitCode, in concrete
the UN/CEFACT Common Code.
"""
import copy
import inspect

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


class Settings:
    CLASSES_TO_IGNORE = 2
    @classmethod
    def superclasses_attributes(cls):
        """
            Returns the superclasses attributes (except object class) and the actual one.
        """
        full_dict = {}
        for superclass in reversed(cls.get_super_classes(cls.CLASSES_TO_IGNORE)):  # We remove object and Settings
            full_dict.update(superclass.actual_attributes())
        return full_dict

    @classmethod
    def _clean(cls, given_dict):
        raise NotImplementedError

    @classmethod
    def get_all_subclasses(cls):
        all_subclasses = []
        for subclass in cls.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(subclass.get_all_subclasses())
        return all_subclasses

    @classmethod
    def get_super_classes(cls, ignore_n):
        return inspect.getmro(cls)[:-ignore_n]

class RDFS(Settings):
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
    def actual_attributes(cls):
        """
        Returns the attributes of only this class.
        """
        full_dict = cls._clean(dict(vars(cls)))
        return full_dict

    @staticmethod
    def __new__(cls, *more):
        """
            Returns all the attributes of all the heriarchy: sub-classess and super-classes. This is the default one used
        """
        full_dict = cls.superclasses_attributes()
        allowed = full_dict['@type']['allowed']
        full_dict.update(cls.subclasses_attributes())
        full_dict['@type']['allowed'] |= allowed
        return full_dict

    @classmethod
    def subclasses_attributes(cls):
        """
            Returns the subclasses' attributes except the actual one.
        """
        full_dictx = {}
        type_allowed = set()
        subtype_allowed = set()
        for subclass in cls.get_all_subclasses():
            attributes = subclass.actual_attributes()
            type_allowed |= attributes.get('@type', {}).get('allowed', set())
            subtype_allowed |= set(attributes.get('type', {}).get('allowed', set()))
            full_dictx.update(attributes)
        if '@type' in full_dictx:
            full_dictx['@type']['allowed'] |= type_allowed
        if 'type' in full_dictx:
            full_dictx['type']['allowed'] |= subtype_allowed
        return full_dictx

    @classmethod
    def _clean(cls, given_dict):
        for key in dict(given_dict).keys():
            if key.startswith('__') or key in ['actual_attributes', 'attributes', '_clean',
                                               'subclasses_attributes', 'resource_name',
                                               'superclasses_attributes', '_settings', 'CLASSES_TO_IGNORE',
                                               'get_all_subclasses', 'get_super_classes', 'type_name']:
                del given_dict[key]
        full_dict = copy.deepcopy(given_dict)
        if '_type' in full_dict:
            full_dict['@type'] = full_dict['_type']
            del full_dict['_type']
            if 'allowed' not in full_dict['@type']:
                full_dict['@type']['allowed'] = {cls.__name__}
        else:
            full_dict['@type'] = copy.deepcopy(RDFS._type)
            full_dict['@type']['allowed'] = {cls.__name__}
        references = []
        from app.event.snapshot.settings import Snapshot
        if cls == Snapshot:
            a = 2
        nested_lookup(full_dict, references, is_sub_type_factory(RDFS))
        for document, ref_key in references:
            document[ref_key] = document[ref_key]()
        return full_dict

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


class ResourceSettings(Settings):
    CLASSES_TO_IGNORE = 3
    @staticmethod
    def __new__(cls):
        attributes = cls.superclasses_attributes()
        if attributes['_schema']:
            attributes['schema'] = attributes['_schema']()
        return attributes

    @classmethod
    def actual_attributes(cls):
        if not hasattr(cls, '_schema'):
            raise TypeError('Resource does not have any schema')
        full_dict = cls._clean(dict(cls.__dict__))
        super_resources = inspect.getmro(cls)[::-3]
        names = [resource._schema.__name__ for resource in super_resources if getattr(resource, '_schema', False)]
        full_dict['url'] = '/'.join([Naming.resource(name) for name in names])
        return full_dict

    @classmethod
    def _clean(cls, given_dict):
        for key in dict(given_dict).keys():
            if key.startswith('__') or key in ('sub_resources', 'resource_name', 'CLASSES_TO_IGNORE', 'get_all_subclasses', 'get_super_classes'):
                del given_dict[key]
        return copy.deepcopy(given_dict)

    @classmethod
    def sub_resources(cls):
        """
        Returns all the sub-resources, without including the actual resource
        """
        return [subclass for subclass in cls.get_all_subclasses() if getattr(subclass, '_schema', False)]

    @classmethod
    def resource_name(cls):
        return cls._schema.resource_name()



