import pymongo

from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.resource import ResourceSettings
from ereuse_devicehub.resources.schema import Thing
from ereuse_devicehub.validation.validation import ALLOWED_WRITE_ROLES


class Account(Thing):
    """
    An account represents a physical person or an organization.
    """

    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.email = email
        self.password = {
            'type': 'string',
            # 'required': True, todo active OR password required
            'minlength': 4,
            'sink': 4,
            'doc': 'Users can only see their own passwords.'
        }
        self.role = {
            'type': 'string',
            'allowed': set(Role.ROLES),
            'default': Role.BASIC,
            'doc': 'See the Roles section to get more info.',
            ALLOWED_WRITE_ROLES: Role.MANAGERS
        }
        self.token = {
            'type': 'string',
            'readonly': True,
        }
        self.name = name
        self.organization = organization
        self.active = {
            'type': 'boolean',
            'default': True,
            'sink': -1,
            'description': 'Activate the account so you can start using it.',
            'doc': 'Inactive accounts cannot login, and they are created through regular events.'
        }
        self.blocked = {
            'type': 'boolean',
            'default': True,
            'sink': -2,
            'description': 'As a manager, you need to specifically accept the user by unblocking it\'s account.',
            ALLOWED_WRITE_ROLES: Role.MANAGERS
        }
        self.isOrganization = isOrganization
        self.databases = {  # todo set allowed for the active databases
            'type': 'databases',
            'required': True,
            ALLOWED_WRITE_ROLES: Role.MANAGERS,
            'teaser': False,
            'sink': -4,
        }
        self.defaultDatabase = {
            'type': 'string',  # todo If this is not set, the first databased in 'databases' it should be used
            ALLOWED_WRITE_ROLES: Role.MANAGERS,
            'teaser': False,
            'sink': -5
        }
        self.fingerprints = {
            'type': 'list',
            'readonly': True,
        }
        self.publicKey = {
            'type': 'string',
            'writeonly': True
        }


class AccountSettings(ResourceSettings):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.resource_methods = ['GET', 'POST']
        self.item_methods = ['PATCH', 'DELETE', 'GET']
        # the standard account entry point is defined as
        # '/accounts/<ObjectId>'. We define  an additional read-only entry
        # point accessible at '/accounts/<username>'.
        # Note that this regex is weak; it will accept more string that are not emails, which is fine; it is fast.
        self.additional_lookup = {
            'url': 'regex("[^@]+@[^@]+\.[^@]+")',
            'field': 'email',
        }
        # 'public_methods': ['POST'],  # Everyone can create an account, which will be blocked (not active)

        self.datasource = {
            'projection': {'token': 0},  # We exclude from showing tokens to everyone
            'source': 'accounts'
        }

        # We also disable endpoint caching as we don't want client apps to
        # cache account data.
        self.cache_control = ''
        self.cache_expires = 0

        # Allow 'token' to be returned with POST responses
        response_fields = ['token', 'email', 'role', 'active', 'name', 'databases', 'defaultDatabase', 'organization',
             'isOrganization']
        self.extra_response_fields = parent.extra_response_fields + response_fields
        # Finally, let's add the schema definition for this endpoint.
        self.schema = Account

        self.mongo_indexes = {
            'email': [('email', pymongo.DESCENDING)],
            'name': [('name', pymongo.DESCENDING)],
            'email and name': [('email', pymongo.DESCENDING), ('name', pymongo.DESCENDING)]
        }

        self.get_projection_blacklist = {  # whitelist has more preference than blacklist
            '*': ('password',),  # No one can see password
            Role.EMPLOYEE: ('active',)  # Regular users cannot see if someone is active or not
        }
        self.get_projection_whitelist = {
            'author': ('password', 'active')  # Except the own author
        }
        self.allowed_item_write_roles = {Role.AMATEUR}  # Amateur can write it's account
        self.use_default_database = True  # We have a common shared database with accounts


# todo this is bad praxis: if a module changes any of the following fields in the domain,
# this won't be reflected for the 'unregistered_user'
# We neeed to make it as an object
email = {
    'type': 'email',
    'required': True,
    'unique': True,
    'sink': 5
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

isOrganization = {
    'type': 'boolean',
    'sink': 2
}

unregistered_user = {
    'email': email,
    'name': name,
    'organization': organization,
    'isOrganization': isOrganization
}
unregistered_user_doc = 'It can be a reference to an account, or a basic account object. ' \
                        + 'The object has to contain at least an e-mail. If the e-mail does ' \
                        + 'not match to an existing one, an account is created. If the e-mail exists, ' \
                        + 'that account is used, and the rest of the data (name, org...) is discarded.'
