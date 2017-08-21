import copy
import inspect
from collections import Sequence
from contextlib import suppress

from ereuse_devicehub.utils import Naming


class Resource:
    """
        Base class for Resources.

        Resources are the URL endpoints of the API, and represent the ontology of DeviceHub. Python-EVE expects us to
        deliver a dictionary with settings of how to configure the resource, including the schema definition.

        We have encapsulated resource settings and their schemas into classes that extend this one, Resource. This is
        our way to implement inheritance between resource schemas and resource settings. An example illustrates better
        the idea:
                                Resource
                    /                       \
                  RDFS                ResourceSettings
                    |           /            |              \
                  Thing       DeviceSettings EventSettings ...
                /   |    \
            Device Event ...

        Thanks to this we do not need to repeat all over again inherited properties.

        Resource provides methods to perform the inheritance, as it is not a classic (pythonic for example) 100%
        inheritance. Please, refer to the methods to get more information.

        Resource is extended by :class:`app.resources.resource.ResourceSettings`
        (which takes care of the settings provided to python-EVE) and
        :class:`app.resources.schema.RDFS` (which provides used RDFS properties, and takes care of the schemas).

        To get a python-EVE ready dictionary, just instantiate the class.
    """

    @staticmethod
    def __new__(cls) -> dict:
        """
            Gets a dictionary with the fields of the resource, ready to use in Python-EVE.
        """
        raise NotImplementedError()

    @classmethod
    def superclasses_fields(cls, top_classes_to_ignore: int) -> dict:
        """
            Returns the superclasses attributes and the actual one.

            This method replaces the attributes of the superclasses that are found in the subclasses.
            This means, for example, that attributes in the actual class with have preference over the one of the
            superclass.
            :param top_classes_to_ignore: Set the top classes to exclude from the attribute gathering. For example, if
            we do not want the values from Object class, as it is the top class, we would set it to 1.
        """
        fields = {}
        for superclass in reversed(cls.superclasses(top_classes_to_ignore)):
            fields.update(superclass.actual_fields())
        return fields

    @classmethod
    def _clean(cls, attributes: dict, attributes_to_remove: Sequence = None) -> dict:
        """
            Obtains a fully new dict only the interesting attributes from a resource.
            This is, removing built-in attributes from python, callables (methods...) and specified attributes.

            Extend this method to do other clean-up stuff with the attributes.
            :param attributes_to_remove: A Collection of attribute names to be removed.
            :returns: A deep copied dictionary
        """
        attributes_to_remove = [] if attributes_to_remove is None else attributes_to_remove
        for key in dict(attributes).keys():
            if key.startswith('__') or key in attributes_to_remove:
                del attributes[key]
            else:
                attribute = getattr(cls, key)
                if callable(attribute) and not (inspect.isclass(attribute) and issubclass(attribute, Resource)):
                    del attributes[key]

        return copy.deepcopy(attributes)

    @classmethod
    def subclasses(cls) -> list:
        """Obtains the subclasses of the actual class, without the actual class."""
        subclasses = []
        for subclass in cls.__subclasses__():
            subclasses.append(subclass)
            subclasses.extend(subclass.subclasses())
        return subclasses

    @classmethod
    def _parent(cls) -> type:
        """Like subclasses, but only getting the direct children, no more descendants."""
        try:
            return cls.superclasses()[1]
        except:
            raise TypeError('Class {} has no parent.'.format(cls.__name__))

    @classmethod
    def superclasses(cls, ignore_n: int = 2) -> tuple:
        """
        :param ignore_n: The number of top superclasses to ignore.
        """
        return inspect.getmro(cls)[:-ignore_n]

    @classmethod
    def actual_fields(cls):
        return cls._clean(dict(vars(cls)), ())

    @classmethod
    def create(cls, name: str, parent_schema: object, schema: dict, parent_resource_settings: object,
               resource_settings: dict) -> (type, type):
        """
        Defines a new resource, setting its endpoint settings and schema.

        Use this method before instantiating the app (app = DeviceHub()). Future work is to avoid this restriction.
        :param name: The name of the resource to create. We append 'Settings' for the settings of the resource.
        :param parent_schema: The parent class to extend, minimum RDFS.
        :param schema: A dict personalizing the schema, or empty dict if using exactly the same schema of the parent.
        :param parent_resource_settings: As 'parent_schema', the ResourceSettings class or subclass to extend from.
        :param resource_settings: As 'schema', for the resource settings.
        """
        # Although it is not very pythonic to register in globals, we are doing so at initialization
        globals()[name] = type(name, (parent_schema,), schema)
        resource_settings_name = '{}Settings'.format(name)
        resource_settings['_schema'] = globals()[name]
        globals()[resource_settings_name] = type(resource_settings_name, (parent_resource_settings,), resource_settings)
        return globals()[name], globals()[resource_settings_name]


class ResourceSettings(Resource):
    # Custom defaults (apart from defined defaults in EVE's settings)
    use_default_database = False
    """Use the user's specific databases or the common default one"""
    extra_response_fields = ['@type', 'label', 'url', 'sameAs', 'description']
    _schema = False
    cache_control = 'max-age=3, must-revalidate'

    @staticmethod
    def __new__(cls) -> dict:
        fields = cls.superclasses_fields(2)  # We ignore Object, Resource
        # We make possible GET the resource (not item) /events/devices/snapshot by providing
        # a default filter. Note that first-level resources (devices) do not use it as there is no need
        # todo write tests for this
        if 'datasource' in fields and len(cls.superclasses(2)) > 2:
            if len(cls.sub_resources()) == 0:
                fields['datasource']['filter'] = {'@type': cls._schema.type_name}
            else:
                fields['datasource']['filter'] = {'@type': {'$in': list(cls._schema.types)}}
        if fields['_schema']:  # We get the schema. This is a costly operation we do not want to do in actual_fields
            with suppress(TypeError):
                fields['parent'] = fields['_schema'].parent_type
            fields['schema'] = fields['_schema']()
        return fields

    @classmethod
    def actual_fields(cls):
        """
            Gets only the actual fields of the class (ignoring parents'), alongside with the URL.
        """
        if not hasattr(cls, '_schema'):
            raise TypeError('Resource does not have any schema')
        fields = super(ResourceSettings, cls).actual_fields()
        super_resources = super(ResourceSettings, cls).superclasses(2)
        # Creating the url for the resource
        # if you set 'url' in the ResourceSettings itself this is used directly as a starting-point
        # This is, the names of the superclassess are replaced
        # If you set 'url' in the schema._settings this is appended in the normal creation of the url
        # instead of the schcema name
        names = []
        for resource in reversed(super_resources):
            if getattr(resource, '_schema', False):
                if getattr(resource, 'url', None):  # If a parent has 'url' we generate the subresource from there
                    names = [resource.url]
                else:
                    names.append(resource._schema._settings.get('url', Naming.resource(resource._schema.__name__)))
        fields['url'] = '/'.join(names)
        return fields

    @classmethod
    def sub_resources(cls):
        """
        Returns all the sub-resources, without including the actual resource
        """
        return [subclass for subclass in cls.subclasses() if getattr(subclass, '_schema', False)]

    @classmethod
    def resource_name(cls):
        return cls._schema.resource_name
