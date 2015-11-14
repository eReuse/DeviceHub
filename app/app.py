from eve import Eve

from app.security.Authentication import RolesAuth
from app.Validation import DeviceHubValidator

app = Eve(auth=RolesAuth, validator=DeviceHubValidator)
