from contextlib import suppress

from ereuse_devicehub.exceptions import StandardError


class Resource:
    """
    Base class for ResourceSettings and Schema. Extend this class and their subclassess to generate hierarchical
    configuration specification, with the objective of generating a python-eve configuration file.

    Resource has three execution times (ordered):
    * init time. When a resource is added through ResourceProxy, ResourceProxy instantiates it __init__() and then
      instantiates all the *ancestors* the resource needs.
    * configuration time. Once all *ancestors* for the given resource are instantiated, ResourceProxy calls config() and
      generates the actual fields for each resource. This is, each instance only generates its own fields. After this,
      you can edit some resource fields by accessing them through the proxy. You should override the config() method
      of your resource to add fields (note that you can access the ancestor's fields, but you won't be updated if
      someone modifies them after, which can be desired or not).
    * dict generation time. Once the resource tree is supposed to be completed (initially when executing app.run())
      the method generate_config() of all resourceSettings is executed, and each resourceSetting and its schema generate
      the configuraiton dict. Override generate_config() in each class to alter this. Here you can access ancestors
      and descendants, with their fields updated.

    If you want to touch any configuration after the dict generation time, you will need to re-generate all the dicts.

    Although you use the python's hierarchical class system to subclass resources, internally it is implemented as
    a tree. This is done as we need special treatment:

    - classes in python are shared in a common process, and we want to different hierarchies and configurations for
      each flask app, so we represent the hierarchy in ResourceProxy .
    - We want to be able to change a field in a parent Resource, and being available to its children instances.
    """

    def __init__(self, proxy, **kwargs):
        """
        Initializes the resource, setting the configuration.

        Do not make any change in proxy here, yet, as not all new resources we instantiated ended up added in the proxy.
        :param proxy: An instance of ResourceProxy where to store
        """
        self.__proxy = proxy
        """The resource this one extends to. If none this is automatically set to 'object'."""
        self.__parent = self.__class__.__bases__[0]

    def config(self, parent=None):
        """
        Override this method to add here your fields.

        Important: *Never call super here*. We will take care of adding the fields of the ancestors.

        :param parent:
        """
        raise NotImplementedError

    @property
    def parent_(self):
        """
        Returns the parent of the resource.

        Note that we provide a parent up to ResourceSetting or RDFS, including them (go to ResourceProxy.add()
        and ResourceProxy.TOP_PARENTS for more details).

        :return Resource The parent.
        :raise ResourceHasNoParent if the resource has no parent.
        """
        try:
            return self.__proxy.parents[self.__class__.__name__]
        except KeyError:
            raise ResourceHasNoParent(self.resource)

    @property
    def children_(self) -> list:
        """Returns the children of the resource."""
        return self.__proxy.children[self.__class__.__name__]

    @property
    def ancestors_(self):
        """Returns an ordered list of ancestors (1st item = parent)"""
        with suppress(ResourceHasNoParent):
            yield self.parent_
            yield from self.parent_.ancestors_

    @property
    def descendants_(self):
        """Returns the descendants"""
        for child in self.children_:
            yield child
            yield from child.descendants_

    # Execute the following methods only after importing all schemas in the proxy
    def __call__(self, *args, **kwargs):
        return self.generate_config()

    def generate_config(self) -> dict:
        """Generates a fully populated dict. Execute this only after importing (executing 'config') of all schemas"""
        fields = {}
        for ancestor in reversed(self.ancestors_):
            fields.update(ancestor.actual_fields)
        fields.update(self.actual_fields)
        return fields

    @property
    def actual_fields(self):
        """
        Returns the fields after doing some clean-up
        """
        fields = dict(vars(self))
        for key in dict(fields).keys():
            field = getattr(self, key)
            if callable(field):  # Is a reference or a schema (if we are a ResourceSettings), let's materialize it
                fields[key] = field()
        return fields

    @property
    def resource(self):
        """The resource name."""
        raise NotImplementedError


class ResourceSettings(Resource):
    """
    IMPORTANT: You need to set self.schema in your self.config() method if you want the resourceSettings to be
    linked to a schema
    """

    def __init__(self, proxy):
        super().__init__(proxy)
        self.__schema_proxy = proxy.schema_proxy

    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        # todo we do not want only the fields of the parent, but of all the ancestors!
        self.use_default_database = False
        """Use the user's specific databases or the common default one"""
        self.extra_response_fields = ['@type', 'label', 'url', 'sameAs', 'description']
        self.cache_control = 'max-age=3, must-revalidate'
        # automatic url generation
        # ex: for HardDrive, it generates 'devices/component/hard-drive'
        names = []
        for ancestor in reversed(self.ancestors_):
            if getattr(ancestor, 'schema', False):
                names.append(ancestor.resource)
        self.url = '/'.join(names)

    @property
    def actual_fields(self):
        fields = super().actual_fields  # This gets us 'schema' too, if set of course
        # We make possible GET the resource (not item) /events/devices/snapshot by providing
        # a default filter. Note that first-level resources (devices) do not use it as there is no need
        # Note that as we need to know how many children we have, this cannot go to self.config()
        if 'datasource' in fields and len(list(self.ancestors_)) > 2:
            if len(self.children_) > 0:
                fields['datasource']['filter'] = {'@type': {'$in': list(self.schema.types)}}
            else:
                fields['datasource']['filter'] = {'@type': self.schema.type}
        return fields

    @property
    def schema(self):
        return self.__schema

    @schema.setter
    def schema(self, schema):
        self.__schema = self.__schema_proxy.add(schema)

    @property
    def resource(self):
        return self.schema.resource


class ResourceHasNoParent(StandardError):
    pass
