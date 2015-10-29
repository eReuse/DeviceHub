from app.Authentication import AccountAuth
from app.Validation import ALLOWED_WRITE_ROLES
from app.config import ROLES, MANAGERS, BASIC

__author__ = 'busta'

account = {
    'email': {
        'type': 'string',
        'required': True,
        'unique': True,
    },
    'password': {
        'type': 'string',
        'required': True,
        'minlength': 4
    },
    'role': {
        'type': 'string',
        'allowed': ROLES,
        'default': BASIC,
        ALLOWED_WRITE_ROLES: MANAGERS
    },
    'token': {
        'type': 'string',
        'readonly': True
    },
    'name': {
        'type': 'string'
    },
    'active': {
        'type': 'boolean',
        'default': False,
        ALLOWED_WRITE_ROLES: MANAGERS
    }
}

account_settings = {
    'resource_methods': ['GET', 'POST', 'DELETE'],
    # the standard account entry point is defined as
    # '/accounts/<ObjectId>'. We define  an additional read-only entry
    # point accessible at '/accounts/<username>'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'email',
    },
    'public_methods': ['POST'],  # Everyone can create an user, which will be blocked (not active)

    'datasource':{
        'projection': {'token': 0}  # We exclude from showing tokens to everyone
    },

    # We also disable endpoint caching as we don't want client apps to
    # cache account data.
    'cache_control': '',
    'cache_expires': 0,

    # Allow 'token' to be returned with POST responses
    'extra_response_fields': ['token', 'email', 'role', 'active', 'name'],


    # Just the author can work with it's account
    #'auth_field': 'user_id',

    # Finally, let's add the schema definition for this endpoint.
    'schema': account,

    'authentication': AccountAuth
}
