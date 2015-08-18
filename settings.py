# This is the default settings loaded by Eve. Don't modify this file to get settings,
# use as said here http://python-eve.org/config.html#development-production


# Please note that MONGO_HOST and MONGO_PORT could very well be left
# out as they already default to a bare bones local 'mongod' instance.
MONGO_DBNAME = 'trading_hub'

from app.device.settings import device_settings
from app.event.settings import event_settings
from app.event.snapshot.settings import snapshot_settings
from app.event.add.settings import add_settings
DOMAIN = {
    #'devices': device_settings,
    #'events': event_settings,
    #'snapshot': snapshot_settings,
    #'add': add_settings
    'his': {}
}

X_DOMAINS = '*'
X_HEADERS = ['Content-Type', 'If-Match']
