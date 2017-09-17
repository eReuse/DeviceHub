"""
DeviceHub app
"""
import inspect
import locale

import flask_cors
import flask_excel
import gnupg
from eve import Eve
from eve.endpoints import schema_collection_endpoint
from eve.exceptions import ConfigException
from eve.io.mongo import GridFSMediaStorage
from eve.io.mongo import MongoJSONEncoder
from eve.render import send_response
from flask import json
from flask import request
from flask_mail import Mail
from inflection import camelize
from shortid import ShortId

from ereuse_devicehub.aggregation.settings import aggregate_view
from ereuse_devicehub.data_layer import DataLayer, MongoEncoder
from ereuse_devicehub.dh_pydash import pydash
from ereuse_devicehub.documents.documents import documents
from ereuse_devicehub.error_handler import ErrorHandlers
from ereuse_devicehub.export.export import export
from ereuse_devicehub.hooks import hooks
from ereuse_devicehub.inventory import inventory
from ereuse_devicehub.mails.mails import mails
from ereuse_devicehub.request import RequestSignedJson
from ereuse_devicehub.resources.account.login.settings import login
from ereuse_devicehub.resources.event.device.live.geoip_factory import GeoIPFactory
from ereuse_devicehub.resources.event.device.register.placeholders import placeholders
from ereuse_devicehub.resources.manufacturers import ManufacturerDomain
from ereuse_devicehub.resources.resource import ResourceSettings
from ereuse_devicehub.resources.submitter.grd_submitter.grd_submitter import GRDSubmitter
from ereuse_devicehub.resources.submitter.submitter_caller import SubmitterCaller
from ereuse_devicehub.scripts.get_manufacturers import ManufacturersGetter
from ereuse_devicehub.security.auth import Auth
from ereuse_devicehub.static import send_device_icon
from ereuse_devicehub.url_parse import UrlParse
from ereuse_devicehub.utils import cache, DeviceHubConfig
from ereuse_devicehub.validation.validation import DeviceHubValidator


class DeviceHub(Eve):
    config_class = DeviceHubConfig

    def __init__(self, import_name=__package__, settings='settings.py', validator=DeviceHubValidator, data=DataLayer,
                 auth=Auth, redis=None, url_converters=None, json_encoder=None, media=GridFSMediaStorage,
                 url_parse=UrlParse, mongo_encoder=MongoEncoder, **kwargs):
        kwargs.setdefault('static_url_path', '/static')
        super().__init__(import_name, settings, validator, data, auth, redis, url_converters, json_encoder, media,
                         **kwargs)
        self.check()
        self.json_encoder = MongoJSONEncoder
        self.request_class = RequestSignedJson
        self.mongo_encoder = mongo_encoder()
        self.gpg = gnupg.GPG()
        self.cache = cache
        self.cache.init_app(self)
        self.sid = ShortId()  # Short id for groups
        self.cross_origin = flask_cors.cross_origin(origins=self.config.get('DOMAINS', '*'),
                                                    expose_headers=self.config['X_EXPOSE_HEADERS'],
                                                    allow_headers=self.config['X_HEADERS'])
        self.url_parse = url_parse()
        flask_excel.init_excel(self)  # required since version 0.0.7
        self.geoip = GeoIPFactory(self)
        hooks(self)  # Set up hooks. You can add more hooks by doing something similar with app "hooks(app)"
        ErrorHandlers(self)
        self.add_cors_url_rule('/login', 'login', view_func=login, methods=('POST', 'OPTIONS'))
        self.add_cors_url_rule('/devices/icons/<file_name>', view_func=send_device_icon)
        self.add_cors_url_rule('/<db>/aggregations/<resource>/<method>', 'aggregation', view_func=aggregate_view)
        self.add_cors_url_rule('/<db>/export/<resource>', view_func=export)
        self.add_cors_url_rule('/<db>/events/<resource>/placeholders', view_func=placeholders, methods=('POST',))
        self.add_cors_url_rule('/<db>/inventory', view_func=inventory)
        self.register_blueprint(documents)
        self.register_blueprint(mails)
        self.mail = Mail(self)
        self._load_jinja_stuff()
        if self.config.get('GRD', True):
            self.grd_submitter_caller = SubmitterCaller(self, GRDSubmitter)
        # Load manufacturers to database if manufacturer's collection in db is empty
        with self.app_context():
            if ManufacturerDomain.count() == 0:
                ManufacturersGetter().execute(self)

    def add_cors_url_rule(self, rule, endpoint=None, view_func=None, **options):
        """
        Like add_url_rule but adding CORS information. Use only for custom flask views as eve's resources already
        handle this.
        """
        return super().add_url_rule(rule, endpoint, self.cross_origin(view_func), **options)

    def register_resource(self, resource: str, settings: ResourceSettings):
        """
            Recursively registers a resource and it's sub-resources.
        """
        if inspect.isclass(settings) and issubclass(settings, ResourceSettings):
            for sub_resource_settings in settings.sub_resources():
                self.register_resource(sub_resource_settings.resource_name(), sub_resource_settings)
            # noinspection PyCallingNonCallable
            new_settings = settings()
        else:
            new_settings = settings
        super().register_resource(resource, new_settings)

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
            SETTINGS_TO_PICK = ('url', 'use_default_database', 'short_description', 'sink', 'icon',
                                'resource_methods', 'item_methods', 'fa', 'parent')
            schemas = json.loads(response.data.decode())
            for resource_type, schema in schemas.items():
                # Note that JSON keys are in camelCase
                schema['_settings'] = pydash.chain(self.config['DOMAIN'][resource_type]) \
                    .pick(SETTINGS_TO_PICK) \
                    .map_keys(lambda _, key: camelize(key, False)) \
                    .value()
        return send_response(None, (schemas,))

    @staticmethod
    def check():
        """Performs startup generic checks"""
        if locale.getpreferredencoding().lower() != 'utf-8':
            """
            Python3 uses by default the system set, but it expects it to be ‘utf-8’ to work correctly.
            An example how to 'fix' it:

            nano .bash_profile and add the following:
            export LC_CTYPE=en_US.UTF-8
            export LC_ALL=en_US.UTF-8
            """
            raise OSError('DeviceHub will only work well with UTF-8 systems, however yours is {}'
                          .format(locale.getpreferredencoding()))

    def _load_jinja_stuff(self):
        """
        Adds global functions and filters for jinja.

        The only way to use regular functions in jinja is by passing them through here and converting them
        to a jinja filter.
        """
        # Filters
        self.jinja_env.filters['pydash_get'] = pydash.get

        self.jinja_env.filters['accountTitle'] = lambda account: account.get('name', account['email'])
        """Gets the name or email of the account."""
        self.jinja_env.filters['resourceTitle'] = lambda r: r['@type'] + ' ' + r.get('label', r['_id'])
        """A title for the resource like 'Event 23' or 'Lot donation of Laura'"""

        # Global functions
        def get_resource_as_string(name, charset='utf-8'):
            # From http://flask.pocoo.org/snippets/77/
            with self.open_resource(name) as f:
                return f.read().decode(charset)

        self.jinja_env.globals['get_resource_as_string'] = get_resource_as_string
