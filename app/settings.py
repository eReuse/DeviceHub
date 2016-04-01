# SERVER_NAME = 'my.server'
# _SERVER_NAME = SERVER_NAME


# Statement for enabling the development environment

# Define the application directory

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.

# Enable protection agains *Cross-site Request Forgery (CSRF)*

# Application settings

# noinspection PyUnresolvedReferences
from settings import *



# Generation of the API (DOMAIN)
from app.resources.device.settings import DeviceSettings
# noinspection PyUnresolvedReferences
from app.resources.device.component import settings
from app.resources.event.settings import EventSettings
from app.resources.account.settings import AccountSettings
from app.resources.place.settings import PlaceSettings
DOMAIN = {
    'devices': DeviceSettings,
    'events': EventSettings,
    'accounts': AccountSettings,
    'places': PlaceSettings
}


RESOURCES_CHANGING_NUMBER = 'device', 'event', 'account', 'place', 'erase'
