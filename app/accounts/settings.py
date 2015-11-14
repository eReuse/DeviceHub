import pymongo

from app.validation import ALLOWED_WRITE_ROLES
from .user import Role

account = {
    'email': {
        'type': 'string',
        'required': True,
        'unique': True
    },
    'password': {
        'type': 'string',
        'required': True,
        'minlength': 4
    },
    'role': {
        'type': 'string',
        'allowed': Role.ROLES,
        'default': Role.BASIC,
        ALLOWED_WRITE_ROLES: Role.MANAGERS
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
        ALLOWED_WRITE_ROLES: Role.MANAGERS
    }
}

account_settings = {
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['PATCH', 'DELETE', 'GET'],
    # the standard account entry point is defined as
    # '/accounts/<ObjectId>'. We define  an additional read-only entry
    # point accessible at '/accounts/<username>'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'email',
    },
    'public_methods': ['POST'],  # Everyone can create an account, which will be blocked (not active)

    'datasource': {
        'projection': {'token': 0}  # We exclude from showing tokens to everyone
    },

    # We also disable endpoint caching as we don't want client apps to
    # cache account data.
    'cache_control': '',
    'cache_expires': 0,

    # Allow 'token' to be returned with POST responses
    'extra_response_fields': ['token', 'email', 'role', 'active', 'name'],

    # Finally, let's add the schema definition for this endpoint.
    'schema': account,

    'mongo_indexes': {
        'email': [('email', pymongo.DESCENDING)],
        'name': [('name', pymongo.DESCENDING)],
        'email and name': [('email', pymongo.DESCENDING), ('name', pymongo.DESCENDING)]
    },

    'get_projection_blacklist': {  # whitelist has more preference than blacklist
        '*': ('password',),  # No one can see password
        Role.EMPLOYEE: ('active',)  # Regular users cannot see if someone is active or not
    },
    'get_projection_whitelist': {
        'author': ('password', 'active')  # Except the own author
    },
    'allowed_item_write_roles': [Role.AMATEUR]  #Amateur can write it's account
}
