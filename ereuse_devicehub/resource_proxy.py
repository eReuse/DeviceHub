from collections import defaultdict
from pydash import find

from ereuse_devicehub.resources.resource import ResourceSettings
from ereuse_devicehub.resources.schema import Schema, RDFS


class ResourceProxy:
    """
    A common pool of instances of Resource. As there can be many flask apps running, each one uses
    two isolated ResourceProxy (one for the ResourceSetting instances and another for Schema instances). Each
    ResourceProxy contains the hierarchy of resources and a way to add and access them.

    To add an instance of resource use add(Class)
    """

    def __init__(self, app):
        self.app = app
        self.resources = {}  # Dict of ClassName: instance of resourceSettings or schemas
        self.parents = {}  # For each resourceSettings or schema, its parent
        self.children = defaultdict(list)  # For each resourceSettings or schema, its children
        self.TOP_PARENTS = [ResourceSettings, RDFS]  # They are the top nodes. They cannot be abstract.

    def add(self, cls):
        """
            Given the class of the resourceSettings or Schema, it adds it if it was not there before.
            :type cls: Resource An instance of resource
            :return The new instance.
        """
        # We make the instance. Note that it is config time and we do not generate the config dict
        resource = cls(self)
        name = resource.name
        if name not in self.resources:
            self.resources[name] = resource
            # We build the double link between the actual node and its parent, if any
            # Note that the top parents are Schema and ResourceSettings, so we do not try to get more parents above them
            parent = None
            if cls not in self.TOP_PARENTS:
                parent_class = resource.__parent  # Hardcoded parent != resource.parent
                parent = find(self.resources, lambda p: isinstance(p, parent_class)) or self.add(parent_class)
                self.children[parent.__name].append(resource)
                self.parents[name] = parent
            resource.config(parent)  # We bundle the fields after having the parent (if any)
        return self.resources[name]

        # Execute the following only after importing all ResourceSettings / schemas

    def generate_config_schema(self, schema_name):
        """Generates the config dict for the given schema"""
        return self.resources[schema_name](self)


class ResourceSettingsProxy(ResourceProxy):
    def __init__(self, app, schema_proxy):
        super().__init__(app)
        self.schema_proxy = schema_proxy


class ResourcesProxy:
    def __init__(self, app):
        self.schema = ResourceProxy(app)
        self.resource_settings = ResourceSettingsProxy(app, self.schema)

    def create_and_add(self, name: str, prefix: str = None, parent_schema: str = None, schema_fields: dict = None,
                       parent_resource_settings: str = None, resource_setting_fields: dict = None):
        """
        Given the name, parents and fields for a resource settings and a schema, it creates classes and adds
        them to the appropriate proxies. Use this method to dynamically add resources.

        :param name: The name of the Schema. We will automatically call the settings *schema + 'Settings'*
        :param prefix: A prefix for the schema, if any.
        :param parent_schema: The name of the schema to use. It needs to be added in the proxy already.
        :param schema_fields: A key, value dict represeting the fields.
        :param parent_resource_settings: As parent_schema but for the resource settings.
        :param resource_setting_fields: As schema_fields but for resource settings. We take care of adding
        the 'schema' field.
        :return:
        """

        def resource_config(fields):
            def config(self):
                """Config method as in Resource.config"""
                for field_name, field_value in fields.items():
                    setattr(self, field_name, field_value)

            return config

        # As per python, any class attribute starting with '__' it is automatically changed to
        # _className__attribute so it is not mixed with inheritors
        schema = type(name, (parent_schema,), {})
        # We implement the Resource.config method, which set the fields from the passed-in dicts
        schema.config = resource_config(schema_fields)
        if prefix:
            schema.prefix = prefix
        resource_settings = type(name + 'Settings', (parent_resource_settings,), {})
        resource_setting_fields['schema'] = schema
        resource_settings.config = resource_config(resource_setting_fields)
        self.resource_settings.add(resource_settings)
