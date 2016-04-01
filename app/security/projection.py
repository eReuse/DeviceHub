from app.app import app
from app.resources.account.user import User

GET_PROJECTION_BLACKLIST = 'get_projection_blacklist'
GET_PROJECTION_WHITELIST = 'get_projection_whitelist'


def project(resource: str, item: dict):
    """
    Projects just the allowed fields for the actual user.

    Use this in resource settings to project just some fields accordingly to some rules and the
    role of the user.

    Both whitelist and blacklist expect a dictionary of tuples. Whitelist overrides the blacklisted
    fields, and the fields that are not shown in blacklist or whitelist are sent to user regularly.
    Every key of the dictionary is a rol or a reserved key, and the tuple is a list of affected fields.

    Example:
    In GET_PROJECTION_BLACKLIST:
    {'role1': ('field1','field2')}
    This means that role1 won't be able to get field1 or field2.

    Then, in GET_PROJECTION_WHITELIST:
    {'author': ('field1',)}
    This means that the author, regardless of the role it has (even if it has role1) will retreive
    field1.

    Reserved keys for blacklist:
    - *: Wildcard. It means all roles.

    Reserved keys for whitelist:
    - author: When scenarios where just the author can get a field. For example, it's password.
            Author is computed using the _id when resource is account or byUser otherwise.
    """

    delete_fields = []
    if 'get_projection_blacklist' in app.config['DOMAIN'][resource]:  # We take note of the blacklisted fields
        blacklist = app.config['DOMAIN'][resource]['get_projection_blacklist']
        for role, fields in blacklist.items():
            if '*' == role or User.actual['role'] <= role:  # Comparing a role means comparing its permission grade
                delete_fields += fields
    if 'get_projection_whitelist' in app.config['DOMAIN'][resource]:  # We remove from the blacklist the white ones
        for role, fields in app.config['DOMAIN'][resource]['get_projection_whitelist'].items():
            if role == 'author':
                if (resource == 'account' and User.actual['_id'] == item['_id']) or ('byUser' in item):
                    delete_fields -= fields
            elif User.actual.role >= role:
                delete_fields -= fields
    for field in delete_fields:  # We delete the blacklisted fields
        if field in item:
            del item[field]
