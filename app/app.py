import os

from .devicehub import Devicehub

from app.security.authentication import RolesAuth
from app.validation import DeviceHubValidator
from app.data_layer import DataLayer

this_directory = os.path.dirname(os.path.realpath(__file__))
settings_file = os.path.abspath(os.path.join(this_directory, '.', 'settings.py'))
app = Devicehub(
    auth=RolesAuth,
    validator=DeviceHubValidator,
    settings=settings_file,
    static_url_path='/static',
    data=DataLayer
)

from hooks import event_hooks

event_hooks(app)

# noinspection PyUnresolvedReferences
from app import error_handler
# noinspection PyUnresolvedReferences
from app.account.login.settings import login
# noinspection PyUnresolvedReferences
from app.static import send_device_icon
