# This is the default settings loaded by Eve. Don't modify this file to get settings,
# use as said here http://python-eve.org/config.html#development-production


# Please note that MONGO_HOST and MONGO_PORT could very well be left
# out as they already default to a bare bones local 'mongod' instance.
MONGO_DBNAME = 'DeviceHub'

from app.device.settings import device_settings, register_parent_devices
from app.event.settings import event_settings, register_events
from app.device.component.settings import register_components, component_settings
from app.accounts.settings import account_settings
from app.place.settings import place_settings
DOMAIN = {
    'devices': device_settings,
    'events': event_settings,
    'component': component_settings,
    'accounts': account_settings,
    'places': place_settings
}
register_parent_devices(DOMAIN)
register_components(DOMAIN)
register_events(DOMAIN)

X_DOMAINS = '*'
X_HEADERS = ['Content-Type', 'Authorization']
X_EXPOSE_HEADERS = ['Authorization']
IF_MATCH = False  # We do not need concurrency control for PUT (if true, we need to prive an etag (include it in x-headers!))

from app.config import ROLES
ALLOWED_ROLES = ROLES
