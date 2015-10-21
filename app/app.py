__author__ = 'busta'
from eve import Eve
from app.Authentication import RolesAuth

app = Eve(auth=RolesAuth)
