from eve import Eve

from app.security.authentication import RolesAuth
from app.validation import DeviceHubValidator

app = Eve(auth=RolesAuth, validator=DeviceHubValidator)

