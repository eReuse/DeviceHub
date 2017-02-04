"""
DeviceHub app
"""
import copy
import os
import sys

import gnupg
from contextlib import suppress
from ereuse_devicehub.aggregation.settings import aggregate_view
from ereuse_devicehub.data_layer import DataLayer
from ereuse_devicehub.error_handler import ErrorHandlers
from ereuse_devicehub.export.export import export
from ereuse_devicehub.hooks import hooks
from ereuse_devicehub.request import RequestSignedJson
from ereuse_devicehub.resource_proxy import ResourcesProxy
from ereuse_devicehub.resources.account.login.settings import login
from ereuse_devicehub.resource_config import resources as _resources
from ereuse_devicehub.resources.submitter.grd_submitter.grd_submitter import GRDSubmitter
from ereuse_devicehub.resources.submitter.submitter_caller import SubmitterCaller
from ereuse_devicehub.security.authentication import RolesAuth
from ereuse_devicehub.static import send_device_icon
from ereuse_devicehub.url_parse import UrlParse
from ereuse_devicehub.utils import cache
from ereuse_devicehub.validation.validation import DeviceHubValidator
from eve import Eve
from eve.endpoints import schema_collection_endpoint
from eve.exceptions import ConfigException
from eve.io.mongo import GridFSMediaStorage
from eve.io.mongo import MongoJSONEncoder
from eve.render import send_response
from flask import json
from flask import request


class DeviceHub(Eve):
    def __init__(self, import_name=__package__, settings='settings.py', validator=DeviceHubValidator, data=DataLayer,
                 auth=RolesAuth, redis=None, url_converters=None, json_encoder=None, media=GridFSMediaStorage,
                 url_parse=UrlParse, resources_proxy=ResourcesProxy, **kwargs):
        kwargs.setdefault('static_url_path', '/static')
        super().__init__(import_name, settings, validator, data, auth, redis, url_converters, json_encoder, media,
                         **kwargs)
        self.json_encoder = MongoJSONEncoder
        self.request_class = RequestSignedJson
        self.gpg = gnupg.GPG()
        self.cache = cache
        self.cache.init_app(self)
        self.url_parse = url_parse()
        # Configure resources
        self.resources = resources_proxy(self)
        _resources(self)
        # Set up hooks
        # You can add more at any time by doing something similar than the following method
        hooks(self)
        ErrorHandlers(self)
        self.add_url_rule('/login', 'login', view_func=login, methods=['POST', 'OPTIONS'])
        self.add_url_rule('/devices/icons/<file_name>', view_func=send_device_icon)
        self.add_url_rule('/<db>/aggregations/<resource>/<method>', 'aggregation', view_func=aggregate_view)
        self.add_url_rule('/<db>/export/<resource>', view_func=export)
        if self.config.get('GRD', True):
            self.grd_submitter_caller = SubmitterCaller(self, GRDSubmitter)

    def run(self, host=None, port=None, debug=None, **options):
        self.set_resources_to_domain()  # Generate the dict for domain and register resources
        super().run(host, port, debug, **options)

    def set_resources_to_domain(self):
        """
        Generates the config fields for the resources, saves them to eve's domain and registers the resources.

        After exeucting app.run(), execute this method any time you modify the configuration Resource instances
        to re-apply them. This method is executed when app.run(), so there is no need to executing it if you
        are adding / modifying resources before app.run() happens.
        :return:
        """
        for resource_settings in self.resource_proxy.resources:
            if hasattr(resource_settings, 'schema'):
                self.config['DOMAIN'][resource_settings.resource] = resource_settings.generate_config()
        # This is extracted from eve's init method.
        domain_copy = copy.deepcopy(self.config['DOMAIN'])
        for resource, settings in domain_copy.items():
            self.register_resource(resource, settings)

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

        self.config.from_object(
            'ereuse_devicehub.default_settings')  # We just add this line todo way to avoid writing all method?

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

    def _init_schema_endpoint(self):
        """Adds '_settings' field to every schema."""
        super()._init_schema_endpoint()
        self.view_functions['schema_collection'] = self._schema_endpoint

    def _schema_endpoint(self):
        """The same as 'schema_collection_endpoint', but adding '_settings' field to every schema."""
        response = schema_collection_endpoint()
        if request.method == 'OPTIONS':
            return response
        else:
            schemas = json.loads(response.data.decode())
            for resource_type, schema in schemas.items():
                settings = self.config['DOMAIN'][resource_type]
                schema['_settings'] = {
                    'url': settings['url'],
                    'use_default_database': settings['use_default_database']
                }
                with suppress(KeyError):
                    schema['_settings']['fa'] = settings['fa']
                with suppress(KeyError):
                    schema['_settings']['short_description'] = settings['short_description']
                with suppress(KeyError):
                    schema['_settings']['sink'] = settings['sink']
                with suppress(KeyError):
                    schema['_settings']['icon'] = settings['icon']
            return send_response(None, (schemas,))
