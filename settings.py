import copy
import os

# User defined settings
# Please note that MONGO_HOST and MONGO_PORT could very well be left
# out as they already default to a bare bones local 'mongod' instance.
MONGO_DBNAME = APP_NAME = 'DeviceHub'
USE_DOCS = False  # Specify if generate api documentation in /docs
DEBUG = True
LOG = False
X_DOMAINS = '*'

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
PAGINATION_DEFAULT = 50
PAGINATION_LIMIT = 100

# Role settings
from app.account.user import Role
#ALLOWED_ROLES = list(Role.ROLES)
ALLOWED_WRITE_ROLES = [Role.AMATEUR]
ALLOWED_ITEM_WRITE_ROLES = [Role.AMATEUR]
ALLOWED_READ_ROLES = [Role.BASIC]
ALLOWED_ITEM_READ_ROLES = [Role.BASIC]

# Generation of the API (DOMAIN)
from app.device.settings import device_settings, register_parent_devices
from app.event.settings import event_settings, register_events
from app.device.component.settings import register_components, component_settings
from app.account.settings import account_settings
from app.place.settings import place_settings
DOMAIN = {
    'devices': device_settings,
    'events': event_settings,
    'component': component_settings,
    'accounts': account_settings,
    'places': place_settings
}
DOMAIN['events']['schema'].update(register_events(DOMAIN))
DOMAIN['component']['schema'].update(register_components(DOMAIN))
full_device_schema = register_parent_devices(DOMAIN)
full_component_copy = copy.deepcopy(DOMAIN['component']['schema'])
full_component_copy['@type']['allowed'] += full_device_schema['@type']['allowed']
full_device_schema.update(full_component_copy)
DOMAIN['devices']['schema'].update(full_device_schema)
