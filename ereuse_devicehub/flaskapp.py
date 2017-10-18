"""
DeviceHub app
"""
import inspect
import locale
from contextlib import contextmanager, suppress
from datetime import timedelta
from typing import Type

import flask_cors
import flask_excel
import gnupg
from eve import Eve
from eve.auth import requires_auth
from eve.endpoints import media_endpoint, schema_collection_endpoint
from eve.exceptions import ConfigException
from eve.io.mongo import GridFSMediaStorage, MongoJSONEncoder
from eve.render import send_response
from flask import json, redirect, request
from flask_mail import Mail
from inflection import camelize
from shortid import ShortId

# noinspection PyUnresolvedReferences
from ereuse_devicehub import helpers
from ereuse_devicehub.aggregation.settings import aggregate_view
from ereuse_devicehub.data_layer import DataLayer, MongoEncoder
from ereuse_devicehub.desktop_app.desktop_app import DesktopApp
from ereuse_devicehub.dh_pydash import pydash
from ereuse_devicehub.documents.documents import documents
from ereuse_devicehub.error_handler import ErrorHandlers
from ereuse_devicehub.export.export import export
from ereuse_devicehub.header_cache import header_cache
from ereuse_devicehub.hooks import hooks
from ereuse_devicehub.inventory import inventory
from ereuse_devicehub.mails.mails import mails
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.account.login.settings import login
from ereuse_devicehub.resources.device.score_condition import Price, Score
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
from ereuse_devicehub.utils import DeviceHubConfig, cache
from ereuse_devicehub.validation.validation import DeviceHubValidator


class DeviceHub(Eve):
    config_class = DeviceHubConfig

    def __init__(self, import_name=__package__, settings='settings.py', validator=DeviceHubValidator, data=DataLayer,
                 auth=Auth, redis=None, url_converters=None, json_encoder=None, media=GridFSMediaStorage,
                 url_parse=UrlParse, mongo_encoder=MongoEncoder, score=Score, price=Price, desktop_app=DesktopApp,
                 **kwargs):
        super().__init__(import_name, settings, validator, data, auth, redis, url_converters, json_encoder, media,
                         **kwargs)
        self.check()
        self.json_encoder = MongoJSONEncoder
        self.mongo_encoder = mongo_encoder()
        self.gpg = gnupg.GPG()
        self.cache = cache
        self.cache.init_app(self)
        self.sid = ShortId()  # Short id for groups
        # Use flask_cors to extend flask's native implementation of options to use cors, for all the endpoints
        # that are not resources.
        flask_cors.CORS(self, origins=self.config.get('DOMAINS', '*'),
                        expose_headers=self.config['X_EXPOSE_HEADERS'],
                        allow_headers=self.config['X_HEADERS'],
                        max_age=self.config['X_MAX_AGE'])
        self.url_parse = url_parse()
        flask_excel.init_excel(self)  # required since version 0.0.7
        self.geoip = GeoIPFactory(self)
        hooks(self)  # Set up hooks. You can add more hooks by doing something similar with app "hooks(app)"
        ErrorHandlers(self)
        self.add_url_rule('/login', 'login', view_func=login, methods=['POST'])
        self.add_url_rule('/devices/icons/<file_name>', view_func=send_device_icon)
        self.add_url_rule('/<db>/aggregations/<resource>/<method>', 'aggregation', view_func=aggregate_view)
        self.add_url_rule('/<db>/export/<resource>', view_func=export)
        self.add_url_rule('/<db>/events/<resource>/placeholders', view_func=placeholders, methods=['POST'])
        self.add_url_rule('/<db>/inventory', view_func=inventory)
        self.before_request(self.redirect_on_browser)
        self.register_blueprint(documents)
        self.register_blueprint(mails)
        self.desktop_app = desktop_app(self)
        self.mail = Mail(self)
        self._load_jinja_stuff()
        if self.config.get('GRD', True):
            self.grd_submitter_caller = SubmitterCaller(self, GRDSubmitter)
        # Load manufacturers to database if manufacturer's collection in db is empty
        with self.app_context():
            if ManufacturerDomain.count() == 0:
                ManufacturersGetter().execute(self)
        # Load RScore and RPrice
        self.score = score(self)
        self.price = price(self)

    def register_resource(self, resource: str, settings: Type[ResourceSettings]):
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

        @contextmanager
        def prefixed_db(db):
            real_url_prefix = self.config['URL_PREFIX']
            if real_url_prefix:
                self.config['URL_PREFIX'] += '/{}'.format(db)
            else:
                self.config['URL_PREFIX'] = db
            yield
            self.config['URL_PREFIX'] = real_url_prefix

        if settings.get('use_default_database', False):
            super()._add_resource_url_rules(resource, settings)
        else:
            for db in self.config['DATABASES']:
                with prefixed_db(db):
                    super()._add_resource_url_rules(resource, settings)

    def _init_media_endpoint(self):
        """
        The media endpoint. In DeviceHub we add database support, authorization and cache headers.
        :return:
        """

        @header_cache(expires=timedelta(weeks=1).total_seconds())
        @requires_auth('')
        def _media_endpoint(db, _id):
            return media_endpoint(_id)

        @header_cache(expires=timedelta(weeks=1).total_seconds())
        def _media_endpoint_open(_id):
            return media_endpoint(_id)

        endpoint = self.config['MEDIA_ENDPOINT']
        if endpoint:
            url = '{}/<db>/{}/<{}:_id>'.format(self.api_prefix, endpoint, self.config['MEDIA_URL'])
            self.add_url_rule(url, 'media', view_func=_media_endpoint)
            url = '{}/{}/<{}:_id>'.format(self.api_prefix, endpoint, self.config['MEDIA_URL'])
            self.add_url_rule(url, 'media-open', view_func=_media_endpoint)

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

    def redirect_on_browser(self):
        """
        Redirects the browsers GETting a resource (anything accepting text/html) to the client webApp.
        :param request:
        """
        if request.method == 'GET' and request.accept_mimetypes.accept_html:
            with suppress(Exception):
                resource_name = request.url_rule.endpoint.split('|')[0]
                self.config['DOMAIN'].get(resource_name)  # Valid resource or exception
                _id = request.view_args['_id']
                db = AccountDomain.requested_database
                url = '{}/inventories/{}/{}.{}'.format(self.config['CLIENT'], db, resource_name, _id)
                return redirect(code=302, location=url)
