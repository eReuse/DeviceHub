import os

import sys
from eve import Eve
from eve.exceptions import ConfigException
from eve.io.mongo import Validator, GridFSMediaStorage, Mongo
from eve.utils import Config

from ereuse_devicehub.resources.resource import ResourceSettings


class DeviceHub(Eve):
    def __init__(self, import_name=__package__, settings='settings.py', validator=Validator, data=Mongo, auth=None,
                 redis=None, url_converters=None, json_encoder=None, media=GridFSMediaStorage, **kwargs):
        super().__init__(import_name, settings, validator, data, auth, redis, url_converters, json_encoder, media,
                         **kwargs)

    def register_resource(self, resource: str, settings: ResourceSettings):
        """
            Recursively registers a resource and it's sub-resources.
        """
        for sub_resource_settings in settings.sub_resources():
            self.register_resource(sub_resource_settings.resource_name(), sub_resource_settings)
        super().register_resource(resource, settings())

    def _add_resource_url_rules(self, resource, settings):
        """
            For the given resources set to work with different databases, it registers as many URL as defined databases
            in the following way:
            For resource 'devices' and db1, db2, ... dn databases:
            - db1/devices
            - db2/devices
            ...
            - dbn/devices

            Check the attribute 'use_default_database' in class :class:`app.resources.resource.ResourceSettings`,
            which forces the resource to just use the default database.
        """
        if settings.get('use_default_database', False):
            super(DeviceHub, self)._add_resource_url_rules(resource, settings)
        else:
            real_url_prefix = self.config['URL_PREFIX']
            for database in self.config['DATABASES']:
                if real_url_prefix:
                    self.config['URL_PREFIX'] += '/{}'.format(database)
                else:
                    self.config['URL_PREFIX'] = database
                super(DeviceHub, self)._add_resource_url_rules(resource, settings)
            self.config['URL_PREFIX'] = real_url_prefix

    def validate_roles(self, directive, candidate, resource):
        """
            The same as eve's, but letting roles to be sets, which is a more adequate type that easies some code.
        """
        roles = candidate[directive]
        if not isinstance(roles, set) and not isinstance(roles, list):
            raise ConfigException("'%s' must be set"
                                  "[%s]." % (directive, resource))

    def load_config(self):
        """
            Same as eve's, just adding our default_settings
        """

        # load defaults
        self.config.from_object('eve.default_settings')

        self.config.from_object('app.default_settings')  # We just add this line todo way to avoid writing all method?

        # overwrite the defaults with custom user settings
        if isinstance(self.settings, dict):
            self.config.update(self.settings)
        else:
            if os.path.isabs(self.settings):
                pyfile = self.settings
            else:
                abspath = os.path.abspath(os.path.dirname(sys.argv[0]))
                pyfile = os.path.join(abspath, self.settings)
            try:
                self.config.from_pyfile(pyfile)
            except IOError:
                # assume envvar is going to be used exclusively
                pass
            except:
                raise

        # overwrite settings with custom environment variable
        envvar = 'EVE_SETTINGS'
        if os.environ.get(envvar):
            self.config.from_envvar(envvar)

