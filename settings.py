import os

# User defined settings
# Please note that MONGO_HOST and MONGO_PORT could very well be left
# out as they already default to a bare bones local 'mongod' instance.
APP_NAME = 'DeviceHub'
USE_DOCS = False  # Specify if generate api documentation in /docs
DEBUG = True
LOG = True
X_DOMAINS = '*'
BASE_PATH_SHOWN_TO_GRD = 'https://devicehub.ereuse.org/'  # Once you send the first device to GRD, always maintain this. Just affects at GRD.
LOGGER = True  # Logger module, which is different from just writing to logs
GRD = True  # GRD is part of logger, so in order for using GRD you need Logger
GRD_DEBUG = False  # GRD module won't send actual data to GRD, rather just log it
URL_PREFIX = ''

# Databases
DATABASES = 'db1', 'db2'  # name showed in the url. As eve, the 'mongoDB prefix'
DB1_DBNAME = 'dh_db1'  # The value is the name used in mongoDB for the database.
DB2_DBNAME = 'dh_db2'

# Logger settings
LOGGER_ACCOUNT = {
    'email': 'logger@ereuse.org',
    'password': '43fa22kaxl0',
}
GRD_ACCOUNT = {
    'username': 'ereuse',
    'password': 'ereuse@grd'
}

# Name of the central DB used only to store 'RESOURCES_USING_DEFAULT_DATABASE'
MONGO_DBNAME = 'dh__accounts'

# From now on you do not need to change anything
# Accounts are the only resource using the default (see above) database
RESOURCES_USING_DEFAULT_DATABASE = 'accounts',

# Schema special resource does not use a database at all
RESOURCES_NOT_USING_CUSTOM_DATABASES = RESOURCES_USING_DEFAULT_DATABASE + ('schema',)

# Other python-eve and flask settings, no need to change them
X_HEADERS = ['Content-Type', 'Authorization']
X_EXPOSE_HEADERS = ['Authorization']
MONGO_QUERY_BLACKLIST = ['$where']
GRD_DOMAIN = 'https://sandbox.ereuse.org/'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
THREADS_PER_PAGE = 2
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"
BULK_ENABLED = False  # Some events cannot work with it todo fix
CSRF_ENABLED = True
IF_MATCH = False  # We do not need concurrency control for PUT (if true, we need to provide an etag (include it in x-headers!))
XML = False  # Will probably cause bugs
CACHE_CONTROL = 'no-cache'  # https://www.mnot.net/cache_docs/
PAGINATION_DEFAULT = 30
PAGINATION_LIMIT = 100
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
SCHEMA_ENDPOINT = 'schema'
EXTRA_RESPONSE_FIELDS = ['@type', 'label']

# Role settings
from app.account.user import Role
#ALLOWED_ROLES = list(Role.ROLES)
ALLOWED_WRITE_ROLES = [Role.AMATEUR]
ALLOWED_ITEM_WRITE_ROLES = [Role.AMATEUR]
ALLOWED_READ_ROLES = [Role.BASIC]
ALLOWED_ITEM_READ_ROLES = [Role.BASIC]

# GRD Settings, do not need to change them
EVENTS_IN_GRD = 'deallocate', 'migrate', 'allocate', 'receive', 'remove', 'add', 'register', 'locate', 'usage-proof', 'recycle'
