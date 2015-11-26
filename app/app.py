import os

from eve import Eve

from app.security.authentication import RolesAuth
from app.validation import DeviceHubValidator

this_directory = os.path.dirname(os.path.realpath(__file__))
settings_file = os.path.abspath(os.path.join(this_directory, '..', 'settings.py'))
app = Eve(auth=RolesAuth, validator=DeviceHubValidator, settings=settings_file, static_url_path='/static')

from hooks import event_hooks

event_hooks(app)

# noinspection PyUnresolvedReferences
from app import error_handler
# noinspection PyUnresolvedReferences
from app.account.login.settings import login
# noinspection PyUnresolvedReferences
from app.static import send_device_icon
