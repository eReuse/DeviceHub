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
import copy

# noinspection PyUnresolvedReferences
from settings import *

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
