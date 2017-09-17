from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.resource import ResourceSettings
from ereuse_devicehub.resources.schema import Thing
from ereuse_devicehub.security.perms import DB_PERMS
from ereuse_devicehub.validation.validation import ALLOWED_WRITE_ROLE


class Account(Thing):
    """
    An account represents a physical person or an organization.
    """
    email = {
        'type': 'email',
        'required': True,
        'unique': True,
        'sink': 5
    }
    password = {
        'type': 'string',
        # 'required': True, todo active OR password required
        'minlength': 4,
        'sink': 4,
        'doc': 'Users can only see their own passwords.'
    }
    role = {
        'type': 'string',
        'allowed': set(Role.ROLES),
        'default': Role.USER,
        'doc': 'See the Roles section to get more info.',
        ALLOWED_WRITE_ROLE: Role(Role.ADMIN)
    }
    token = {
        'type': 'string',
        'readonly': True,
    }
    name = {
        'type': 'string',
        'sink': 3,
        'description': 'The name of an account, if it is a person or an organization.'
    }
    organization = {
        'type': 'string',
        'sink': 1,
        'description': 'The name of the organization the account is in. Organizations can be inside others.'
    }
    active = {
        'type': 'boolean',
        'default': True,
        'sink': -1,
        'description': 'Activate the account so you can start using it.',
        'doc': 'Inactive accounts cannot login, and they are created through regular events.'
    }
    blocked = {
        'type': 'boolean',
        'default': True,
        'sink': -2,
        'description': 'As a manager, you need to specifically accept the user by unblocking it\'s account.',
        ALLOWED_WRITE_ROLE: Role(Role.ADMIN)
    }
    isOrganization = {
        'type': 'boolean',
        'sink': 2
    }
    databases = {  # todo make admin worthy
        'type': 'dict',
        'valueschema': {
            'type': 'string',
            'allowed': list(DB_PERMS)
        },
        'required': True,
        ALLOWED_WRITE_ROLE: Role(Role.ADMIN),
        'teaser': False,
        'sink': -4,
    }
    defaultDatabase = {
        'type': 'string',  # todo If this is not set, the first databased in 'databases' it should be used
        ALLOWED_WRITE_ROLE: Role(Role.ADMIN),
        'teaser': False,
        'sink': -5
    }
    shared = {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'db': {
                    'type': 'string'
                },
                '@type': {
                    'type': 'string'
                },
                'label': {
                    'type': 'string'
                },
                '_id': {
                    'type': 'string'
                },
                'baseUrl': {
                    'type': 'url',
                    'doc': 'The scheme, domain, any path to reach the DeviceHub.'
                }
            }
        },
        'default': [],
        'materialized': True,
        'description': 'The groups (eg: lots, packages...) other people shared to this account.'
    }
    fingerprints = {
        'type': 'list',
        'readonly': True,
    }
    publicKey = {
        'type': 'string',
        'writeonly': True
    }


class AccountSettings(ResourceSettings):
    resource_methods = ['GET', 'POST']
    item_methods = ['PATCH', 'DELETE', 'GET']
    # the standard account entry point is defined as
    # '/accounts/<ObjectId>'. We define  an additional read-only entry
    # point accessible at '/accounts/<username>'.
    # Note that this regex is weak; it will accept more string that are not emails, which is fine; it is fast.
    additional_lookup = {
        'url': 'regex("[^@]+@[^@]+\.[^@]+")',
        'field': 'email',
    }
    # 'public_methods': ['POST'],  # Everyone can create an account, which will be blocked (not active)

    datasource = {
        'projection': {'token': 0},  # We exclude from showing tokens to everyone
        'source': 'accounts'
    }

    # We also disable endpoint caching as we don't want client apps to
    # cache account data.
    cache_control = ''
    cache_expires = 0

    # Allow 'token' to be returned with POST responses
    extra_response_fields = ResourceSettings.extra_response_fields + ['email', 'active', 'name',
                                                                      'databases', 'defaultDatabase', 'organization',
                                                                      'isOrganization']

    # Finally, let's add the schema definition for this endpoint.
    _schema = Account

    allowed_write_roles = {Role.ADMIN}  # Only admins or above can POST, PUT or DELETE
    use_default_database = True  # We have a common shared database with accounts
    fa = 'fa-user-o'


unregistered_user = {
    'email': Account.email,
    'name': Account.name,
    'organization': Account.organization,
    'isOrganization': Account.isOrganization
}
unregistered_user_doc = 'It can be a reference to an account, or a basic account object. ' \
                        + 'The object has to contain at least an e-mail. If the e-mail does ' \
                        + 'not match to an existing one, an account is created. If the e-mail exists, ' \
                        + 'that account is used, and the rest of the data (name, org...) is discarded.'
