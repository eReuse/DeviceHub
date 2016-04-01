from eve import Eve
from eve.exceptions import ConfigException

from app.resources.resource import ResourceSettings


class DeviceHub(Eve):
    def register_resource(self, resource: str, settings: ResourceSettings):
        """
            Recursively registers a resource and it's sub-resources.

        """

        for sub_resource_settings in settings.sub_resources():
            self.register_resource(sub_resource_settings.resource_name(), sub_resource_settings)
        super().register_resource(resource, settings())

    def _add_resource_url_rules(self, resource, settings):
        if resource in self.config['RESOURCES_USING_DEFAULT_DATABASE']:
            super(DeviceHub, self)._add_resource_url_rules(resource, settings)
        else:
            real_url_prefix = self.config['URL_PREFIX']
            for database in self.config['DATABASES']:
                self.config['URL_PREFIX'] = database
                super(DeviceHub, self)._add_resource_url_rules(resource, settings)
            self.config['URL_PREFIX'] = real_url_prefix

    def validate_roles(self, directive, candidate, resource):
        """ Validates that user role directives are syntactically and formally
        adeguate.

        :param directive: either 'allowed_[read_|write_]roles' or
                          'allow_item_[read_|write_]roles'.
        :param candidate: the candidate setting to be validated.
        :param resource: name of the resource to which the candidate settings
                         refer to.

        .. versionadded:: 0.0.4
        """
        roles = candidate[directive]
        if not isinstance(roles, set) and not isinstance(roles, list):
            raise ConfigException("'%s' must be set"
                                  "[%s]." % (directive, resource))