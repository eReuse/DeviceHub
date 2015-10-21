from app.Authentication import AccountAuth

__author__ = 'busta'

account = {
    'username': {
        'type': 'string',
        'required': True,
        'unique': True,
    },
    'password': {
        'type': 'string',
        'required': True,
    },
    'roles': {
        'type': 'list',
        'allowed': ['user', 'superuser', 'admin'],
        'required': True,
    },
    'token': {
        'type': 'string',
        'required': True,
    }
}

account_settings = {
    # the standard account entry point is defined as
    # '/accounts/<ObjectId>'. We define  an additional read-only entry
    # point accessible at '/accounts/<username>'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username',
    },

    # We also disable endpoint caching as we don't want client apps to
    # cache account data.
    'cache_control': '',
    'cache_expires': 0,

    # Allow 'token' to be returned with POST responses
    'extra_response_fields': ['token'],


    # Just the author can work with it's account
    #'auth_field': 'user_id',

    # Finally, let's add the schema definition for this endpoint.
    'schema': account,

#    'authentication': AccountAuth
}
