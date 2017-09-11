# An initial idea of {account_id: [perm1, perm2], ...} was done for this
# but then mongo can't use indexes, and querying this needs to be very fast

# Permissions for resources
READ = 'r'
EDIT = 'e'
RESTRICTED_EDIT = 're'
ADMIN = 'ad'
ACCESS = 'ac'
PARTIAL_ACCESS = 'pa'
RESOURCE_PERMS = {READ, EDIT, RESTRICTED_EDIT, ADMIN}
DB_PERMS = {ACCESS, PARTIAL_ACCESS, ADMIN}
EXPLICIT_DB_PERMS = {ACCESS, ADMIN}

perms = {
    'type': 'list',
    'schema': {
        'type': 'dict',
        'schema': {
            'account': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'accounts',
                    'field': '_id',
                    'embeddable': True
                },
                'required': True
            },
            'perm': {
                'type': 'string',
                'required': True,
                'allowed': RESOURCE_PERMS
            }
        }
    },
    'default': [],
    'description': 'The permissions accounts have on the resource.',
    'doc': 'These permissions are set on groups, and their children inherit them.'
           'Apart from this, accounts can have access to resources if they have access to the entire database, too.'
           'That access is stored in the Account *databases* field.'
}

# todo can we add this as perms[].explicit = True / False? see implications
explicit = {
    'type': 'list',
    'schema': {
        'type': 'string',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True
        }
    },
    'default': [],
    'description': 'The accounts that someone explicitly shared them the item.',
    'doc': 'This will be empty for resources that inherited the permissions.'
}
