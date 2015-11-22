# This is the default settings loaded by Eve. Don't modify this file to get settings,
# use as said here http://python-eve.org/config.html#development-production


# Please note that MONGO_HOST and MONGO_PORT could very well be left
# out as they already default to a bare bones local 'mongod' instance.
import copy
import os

MONGO_DBNAME = 'DeviceHub'

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

MONGO_QUERY_BLACKLIST = ['$where']
BULK_ENABLED = False

X_DOMAINS = '*'
X_HEADERS = ['Content-Type', 'Authorization']
X_EXPOSE_HEADERS = ['Authorization']
IF_MATCH = False  # We do not need concurrency control for PUT (if true, we need to prive an etag (include it in x-headers!))
XML = False

from app.account.user import Role


#ALLOWED_ROLES = list(Role.ROLES)
ALLOWED_WRITE_ROLES = [Role.AMATEUR]
ALLOWED_ITEM_WRITE_ROLES = [Role.AMATEUR]
ALLOWED_READ_ROLES = [Role.BASIC]
ALLOWED_ITEM_READ_ROLES = [Role.BASIC]
__author__ = 'Xavier'
APP_NAME = "DeviceHub"
ENCODING = "utf-8"  # used just in some scenarios where default Flask doesn't happen (default is utf-8)
_SERVER_NAME = "https://devicehub.ereue.org"  # Name used not by flask or python-eve but for sending it to other servers (can be false :-D)
GRD_DOMAIN = 'https://sandbox.ereuse.org/'
DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
THREADS_PER_PAGE = 2
CSRF_ENABLED = True
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"