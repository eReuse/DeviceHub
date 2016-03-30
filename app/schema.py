"""
We mimic https://schema.org/unitCode, in concrete
the UN/CEFACT Common Code.
"""
import copy
import inspect

from app.utils import Naming


class UnitCodes:
    mbyte = '4L'
    mbps = 'E20'
    mhz = 'MHZ'
    gbyte = 'E34'
    ghz = 'A86'
    bit = 'A99'
    kgm = 'KGM'
    m = 'MTR'


class RDFS:
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

    @classmethod
    def actual_attributes(cls):
        """
        Returns the attributes of only this class.
        """
        full_dict = dict(cls.__dict__)
        cls._clean(full_dict)
        if '@type' in full_dict:
            if 'allowed' not in full_dict['@type']:
                full_dict['@type']['allowed'] = [cls.__name__]
        else:
            full_dict['@type'] = RDFS._type
            full_dict['@type']['allowed'] = [cls.__name__]
        return full_dict

    @staticmethod
    def __new__(cls, *more):
        """
            Returns all the attributes of all the heriarchy: sub-classess and super-classes. This is the default one used
        """
        full_dict = cls.superclasses_attributes()
        full_dict.update(cls.subclasses_attributes())
        return full_dict

    @classmethod
    def superclasses_attributes(cls):
        """
            Returns the superclasses attributes (except object class) and the actual one.
        """
        full_dict = {}
        for superclass in reversed(inspect.getmro(cls)[:-1]):
            full_dict.update(superclass.actual_attributes())
        return full_dict

    @classmethod
    def subclasses_attributes(cls):
        """
            Returns the subclasses' attributes except the actual one.
        """
        full_dict = {}
        type_allowed = []
        for subclass in get_all_subclasses(cls):
            attributes = subclass.actual_attributes()
            type_allowed += attributes.get('@type', [])
            full_dict.update(attributes)
        if '@type' in full_dict:
            full_dict['@type']['allowed'] += type_allowed
        return full_dict

    @staticmethod
    def _clean(full_dict):
        for key in dict(full_dict).keys():
            if key.startswith('__') or key in ['actual_attributes', 'attributes', '_clean',
                                               'subclasses_attributes', 'resource_name',
                                               'superclasses_attributes']:
                del full_dict[key]
        if '_type' in full_dict:
            full_dict['@type'] = full_dict['_type']
            del full_dict['_type']

    @classmethod
    def resource_name(cls):
        return Naming.resource(cls.__name__)


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


class ResourceSettings:
    @staticmethod
    def __new__(cls, *more):
        if not hasattr(cls, '_schema'):
            raise TypeError('Resource does not have any schema')
        full_dict = dict(cls.__dict__)
        for key in cls.__dict__.keys():
            if key.startswith('__') or key in ('sub_resources',):
                del full_dict[key]
        full_dict['schema'] = full_dict['_schema']()
        del full_dict['_schema']
        super_resources = inspect.getmro(cls)[::-1]
        names = [resource.__name__ for resource in super_resources if getattr(resource, '_schema', False)]
        full_dict['url'] = '/'.join([Naming.resource(name) for name in names])
        full_dict['datasource'] = full_dict['datasource'] if 'datasource' in full_dict else {}
        full_dict['datasource']['source'] = Naming.resource(names[-1])
        full_dict['datasource']['filter'] = {'@type': {'$eq': names[-1]}}
        return full_dict

    @classmethod
    def sub_resources(cls):
        """
        Returns all the sub-resources, without including the actual resource
        """
        return [subclass for subclass in cls.__subclasses__() if getattr(subclass, '_schema', False)]

    @classmethod
    def resource_name(cls):
        try:
            return cls._schema.resource_name()
        except Exception as e:
            a = 2


def get_all_subclasses(cls):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses