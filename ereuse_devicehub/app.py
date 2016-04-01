from os import path

import gnupg
from eve.io.mongo import MongoJSONEncoder
from flask.ext.cache import Cache

from ereuse_devicehub.data_layer import DataLayer
from ereuse_devicehub.request import RequestSignedJson
from ereuse_devicehub.security.authentication import RolesAuth
from ereuse_devicehub.validation import DeviceHubValidator
from devicehub_class_diagram import DeviceHubClassDiagram
from .flaskapp import DeviceHub

this_directory = path.dirname(path.realpath(__file__))
settings_file = path.abspath(path.join(this_directory, '.', 'settings.py'))
app = DeviceHub(
    auth=RolesAuth,
    validator=DeviceHubValidator,
    settings=settings_file,
    static_url_path='/static',
    data=DataLayer
)
app.json_encoder = MongoJSONEncoder
app.request_class = RequestSignedJson
app.gpg = gnupg.GPG()
DeviceHubClassDiagram(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

from hooks import event_hooks

event_hooks(app)

# noinspection PyUnresolvedReferences
from ereuse_devicehub import error_handler
# noinspection PyUnresolvedReferences
from ereuse_devicehub.resources.account.login.settings import login
# noinspection PyUnresolvedReferences
from ereuse_devicehub.static import send_device_icon
# noinspection PyUnresolvedReferences
from ereuse_devicehub.aggregation.settings import aggregate_view
