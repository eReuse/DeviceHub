__author__ = 'busta'
from eve import Eve
from app.Authentication import RolesAuth
from app.Validation import DeviceHubValidator


app = Eve(auth=RolesAuth, validator=DeviceHubValidator)