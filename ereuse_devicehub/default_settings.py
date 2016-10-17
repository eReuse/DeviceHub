"""
    Default API settings. Override them in a separate file, exactly as done in python-eve.

    These settings overrides eve's default configuration, and adds new ones.
"""
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.utils import Naming

CLIENT = None
"""
    The base URL of DeviceHubClient or any other compatible client. The server redirects browsers to this URL.
    Do not add final trailing slash.
    Example: https://www.devicetag.io
"""

GRD = True  # GRD is part of logger, so in order for using GRD you need Logger
"""Activates the GRD Submitter."""
GRD_DEBUG = False
"""Do not really send data to GRD, just print it on screen and log it in a file."""
BASE_PATH_SHOWN_TO_GRD = None
"""
    The base URL shown to GRD when submitting data. It is supposed to be the base URL that this DeviceHub listents on.
    Add final trailing slash.
    Example: https://api.devicetag.io/
"""

# Databases
DATABASES = 'db1',
"""Sets the name of the databases, as appear in the URL. This is the 'mongoDB prefix of eve."""
DB1_DBNAME = 'dh_db1'  # The value is the name used in mongoDB for the database.
"""Sets the name of the database, as it is stored in mongoDB. Each database set in 'DATABASES' needs to have this variable."""
MONGO_DBNAME = 'dh__accounts'
"""
    Name of the central DB used only to store resources set with
    :attr:`app.resources.ResourceSettings.use_default_database
"""
RESOURCES_NOT_USING_DATABASES = ['schema']
"""List of any special resources that do not use any database, for example eve's schema endpoint."""
RESOURCES_CHANGING_NUMBER = {'device', 'event', 'account', 'place', 'erase', 'project'}
"""
    List of resources that change form singular and plural. Write it in the resource singular form.
    See :class:`app.utils.Naming`
"""

# Submitter settings
SUBMITTER_ACCOUNT = {
    'email': 'logger@ereuse.org',
    'password': '43fa22kaxl0',
}
"""The account Logger module uses to interact with DeviceHub. The account is created if it doesn't exist."""
GRD_ACCOUNT = {
    'username': None,
    'password': None
}
"""The account DeviceHub uses to send data to GRD. eReuse.org provides this account on demand."""

# Other python-eve and flask settings, no need to change them
X_HEADERS = ['Content-Type', 'Authorization']
X_EXPOSE_HEADERS = ['Authorization']
MONGO_QUERY_BLACKLIST = ['$where']
GRD_DOMAIN = 'https://sandbox.ereuse.org'
THREADS_PER_PAGE = 2
BULK_ENABLED = False  # Some events cannot work with it todo fix
CSRF_ENABLED = True
IF_MATCH = False  # We do not need concurrency control for PUT (if true, we need to provide an etag (include it in x-headers!))
XML = False  # Will probably cause bugs
# 12 hours of cache for /schema, resources have their own cache in their ResourceSettings
# See https://www.mnot.net/cache_docs/ for more info with cache
CACHE_CONTROL = 'private, max-age=' + str(60 * 60 * 12)
PAGINATION_DEFAULT = 30
PAGINATION_LIMIT = 100
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
SCHEMA_ENDPOINT = 'schema'
VALIDATION_ERROR_AS_LIST = True  # We always use list to show errors
ITEM_CACHE = 120  # We differentiate from Resource cache (Cache setting from Eve) from Item cache

# Role settings
from ereuse_devicehub.resources.account.role import Role

ALLOWED_WRITE_ROLES = {Role.AMATEUR}
ALLOWED_ITEM_WRITE_ROLES = {Role.AMATEUR}
ALLOWED_READ_ROLES = {Role.BASIC}
ALLOWED_ITEM_READ_ROLES = {Role.BASIC}

# GRD Settings, do not change them
_events_in_grd = ('Deallocate', 'Migrate', 'Allocate', 'Receive',
                  'Remove', 'Add', 'Register', 'Locate', 'UsageProof', 'Recycle')
EVENTS_IN_GRD = [Naming.resource(DeviceEventDomain.new_type(event)) for event in _events_in_grd]
# Generation of the API (DOMAIN)
from ereuse_devicehub.resources.device.settings import DeviceSettings
from ereuse_devicehub.resources.account.settings import AccountSettings
from ereuse_devicehub.resources.event.settings import EventSettings
from ereuse_devicehub.resources.place.settings import PlaceSettings

DOMAIN = {
    'devices': DeviceSettings,
    'events': EventSettings,
    'accounts': AccountSettings,
    'places': PlaceSettings
}
