import pymongo

from app.validation import ALLOWED_WRITE_ROLES
from settings import DATABASES
from .user import Role

account = {
    'email': {
        'type': 'email',
        'required': True,
        'unique': True,
        'sink': 5
    },
    'password': {
        'type': 'string',
        #'required': True, todo active OR password required
        'minlength': 4,
        'sink': 4
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
        'type': 'string',
        'sink': 3
    },
    'organization': {
        'type': 'string',
        'sink': 1
    },
    '@type': {
        'type': 'string',
        'default': 'Account',
        'allowed': ['Account'],
        'sink': 0
    },
    'active': {
        'type': 'boolean',
        'default': True,
        'sink': -1,
        'description': 'Activate the account so you can start using it.'  # Accounts created through an event are inactive
    },
    'blocked': {
        'type': 'boolean',
        'default': True,
        'sink': -2,
        'description': 'As a manager, you need to specifically accept the user by unblocking it\'s account.',
        ALLOWED_WRITE_ROLES: Role.MANAGERS
    },
    'isOrganization': {
        'type': 'boolean',  # If is an organization,  name needs to be filled, too
        'sink': 2
    },
    'databases': {
        'type': 'list',
        'required': True,
        'allowed': list(DATABASES),
        ALLOWED_WRITE_ROLES: Role.MANAGERS,
        'sink': -4
    },
    'defaultDatabase': {
        'type': 'string',  # todo If this is not set, the first databased in 'databases' it should be used
        ALLOWED_WRITE_ROLES: Role.MANAGERS,
        'sink': -5
    },
    'fingerprints': {
        'type': 'list',
        'readonly': True,
    },
    'publicKey': {
        'type': 'string',
        'writeonly': True
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
    #'public_methods': ['POST'],  # Everyone can create an account, which will be blocked (not active)

    'datasource': {
        'projection': {'token': 0}  # We exclude from showing tokens to everyone
    },

    # We also disable endpoint caching as we don't want client apps to
    # cache account data.
    'cache_control': '',
    'cache_expires': 0,

    # Allow 'token' to be returned with POST responses
    'extra_response_fields': ['token', 'email', 'role', 'active', 'name', 'databases'],

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
    'allowed_item_write_roles': [Role.AMATEUR]  # Amateur can write it's account
}


unregistered_user = {
    'email': account['email'],
    'name': account['name'],
    'organization': account['organization'],
    'isOrganization': account['isOrganization']
}
