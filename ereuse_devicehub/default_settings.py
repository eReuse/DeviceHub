"""
    Default API settings. Override them in a separate file, exactly as done in python-eve.

    These settings overrides eve's default configuration, and adds new ones.
"""
from datetime import timedelta

from pymongo import ASCENDING, DESCENDING, HASHED, IndexModel
from pymongo.collation import Collation, CollationStrength

from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.account.settings import AccountSettings
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.settings import DeviceSettings
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.settings import EventSettings
from ereuse_devicehub.resources.group.abstract.lot.domain import LotDomain
from ereuse_devicehub.resources.group.group_log.settings import GroupLogEntrySettings
from ereuse_devicehub.resources.group.physical.package.domain import PackageDomain
from ereuse_devicehub.resources.group.physical.pallet.domain import PalletDomain
from ereuse_devicehub.resources.group.physical.place.domain import PlaceDomain
from ereuse_devicehub.resources.group.settings import GroupSettings
from ereuse_devicehub.resources.manufacturers import ManufacturerDomain, ManufacturerSettings
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
BASE_URL_FOR_AGENTS = 'https://devicehub.ereuse.org'
"""
    This is the URL showed to other agents, like GRD or other DeviceTags, DO NOT CHANGE IT AFTER FIRST USE.
    Add final trailing slash.
    Example: https://api.devicetag.io/
"""

# Databases
DATABASES = 'db1',
"""Sets the name of the databases, as appear in the URL. This is the 'mongoDB prefix of eve."""
DB1_DBNAME = 'dh_db1'  # The value is the name used in mongoDB for the database.
"""
Sets the name of the database, as it is stored in mongoDB. Each database set in 'DATABASES'
needs to have this variable.
"""
MONGO_DBNAME = 'dh__accounts'
"""
    Name of the central DB used only to store resources set with
    :attr:`app.resources.ResourceSettings.use_default_database
"""
RESOURCES_NOT_USING_DATABASES = ['schema']
"""List of any special resources that do not use any database, for example eve's schema endpoint."""
RESOURCES_CHANGING_NUMBER = {'device', 'event', 'account', 'place', 'erase', 'project', 'package', 'lot',
                             'manufacturer', 'pallet'}
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
BULK_ENABLED = False  # Some events cannot work with it
CSRF_ENABLED = True
# We do not need concurrency control for PUT (if true, we need to provide an etag (include it in x-headers!))
IF_MATCH = False
XML = False  # Will probably cause bugs
# 12 hours of cache for /schema, resources have their own cache in their ResourceSettings
# See https://www.mnot.net/cache_docs/ for more info with cache
CACHE_CONTROL = 'private, max-age=' + str(60 * 60 * 12)
PAGINATION_DEFAULT = 30
PAGINATION_LIMIT = 100
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
SECONDARY_DATE_FORMAT = DATE_FORMAT + '.%fZ'
SCHEMA_ENDPOINT = 'schema'
VALIDATION_ERROR_AS_LIST = True  # We always use list to show errors
ITEM_CACHE = 120  # We differentiate from Resource cache (Cache setting from Eve) from Item cache
TIME_TO_DELETE_RESOURCES = timedelta(minutes=5)  # How much time do users have to delete a resource after creating it?
BANDWIDTH_SAVER = False  # Returns all fields in POST

# GRD Settings, do not change them
_events_in_grd = ('Deallocate', 'Migrate', 'Allocate', 'Receive',
                  'Remove', 'Add', 'Register', 'Locate', 'UsageProof', 'Recycle')
EVENTS_IN_GRD = [Naming.resource(DeviceEventDomain.new_type(event)) for event in _events_in_grd]

# Files
# From http://python-eve.org/features.html#serving-media-files-at-a-dedicated-endpoint
RETURN_MEDIA_AS_BASE64_STRING = False
RETURN_MEDIA_AS_URL = True
MULTIPART_FORM_FIELDS_AS_JSON = True
AUTO_COLLAPSE_MULTI_KEYS = True
AUTO_CREATE_LISTS = True
EXTENDED_MEDIA_INFO = ['content_type', 'name', 'length']

# Resources
DOMAIN = {
    'devices': DeviceSettings,
    'events': EventSettings,
    'accounts': AccountSettings,
    'groups': GroupSettings,
    'manufacturers': ManufacturerSettings,
    'group-log-entry': GroupLogEntrySettings
}

# Indexing
_INSENSITIVE = Collation('en_US', strength=CollationStrength.SECONDARY)
PERMS_INDEX = ('perms.account', ASCENDING), ('perms.perm', ASCENDING)
"""Insensitive caps and accents collation, suited for searches with $regex of single text fields"""
_DESCENDING_UPDATE = ('_updated', DESCENDING),
_GROUP_INDEXES = [
    IndexModel(_DESCENDING_UPDATE, name='default group view'),
    IndexModel(_DESCENDING_UPDATE + PERMS_INDEX, name='default group view with perms'),
    IndexModel((('ancestors.lots', HASHED),), name='all lots ancestors'),
    IndexModel('label', name='ranged label searches', collation=_INSENSITIVE, background=True)
]
INDEXES = [
    (ManufacturerDomain, [IndexModel('label', name='ranged label searches', collation=_INSENSITIVE)]),
    (AccountDomain, [IndexModel('email', name='ranged email searches', collation=_INSENSITIVE)]),
    (
        DeviceDomain,
        [
            IndexModel((('@type', ASCENDING), ('events.@type', ASCENDING), ('events._updated', DESCENDING)),
                       name='default device info'),
            IndexModel(PERMS_INDEX, name='perms')
        ]
    ),
    (
        DeviceEventDomain,
        [
            IndexModel((('device', HASHED),), name='device relationship'),
            IndexModel('devices', name='devices relationship'),
            IndexModel('components', name='components relationship')
        ]
    ),
    (LotDomain, _GROUP_INDEXES),
    (PackageDomain, _GROUP_INDEXES),
    (PalletDomain, _GROUP_INDEXES),
    (PlaceDomain, _GROUP_INDEXES)
]
"""
Mongo indexes. Drawback of defining in ResourceSettings would be inheriting all indexes for children resources,
so instead we define them here one time for each collection, by defining any domain that uses that collection.
For example, DeviceDomain acts on 'devices' collection, so we define its events there, but we don't need to re-define
the indexes for ComponentDomain, as they use the same db. For Group is otherwise; each type of group works in each
type of collection and need their indexes set especially.

Note we don't use eve 'mongo_indexes' as they are not database (inventory) aware and they are re-computed every time
the app starts (even eve docs do not recommend using them in big apps).

Instead, our indexes are re-set and re-computed only in specific Update scripts that require it (usually software
updates that modify indexes).  
"""


R_PACKAGES_PATH = None
"""
Location of the directory where the R packages that DeviceHub need (and only those) are installed. 
Set None to use R's default directory. Useful to isolate your DeviceHub instance and when having to deal with
different users (looking at you apache's www-data) executing the same thing. 
"""
