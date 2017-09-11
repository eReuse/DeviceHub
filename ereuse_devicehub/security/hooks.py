from contextlib import suppress

from bson import ObjectId
from flask import current_app
from pydash import find

from ereuse_devicehub.exceptions import InsufficientDatabasePerm
from ereuse_devicehub.resources.account.domain import AccountDomain, NotADatabase
from ereuse_devicehub.resources.account.settings import Account
from ereuse_devicehub.security.perms import READ


def check_perms_for_list_of_items(_, __, lookup: dict):
    """Ensure user has sufficient permission to GET the resources."""
    # Are we querying a list of resources? (eg: www.ex.com/foo?where={})
    if type(lookup.get('_id', None)) not in {ObjectId, int, str}:
        # has_full_db_access will throw notADatabase for endpoints that
        # do not use specific databases, but we don't care for those
        with suppress(NotADatabase):
            if not current_app.auth.has_full_db_access():
                # Only get resources that the user has READ access to
                lookup['perms'] = {'$elemMatch': {'account': AccountDomain.actual['_id'], 'perm': READ}}


def check_perms_for_item(resource_name: str, resource: dict):
    """Ensure user has sufficient permission to GET a **specific** resource."""
    if '_items' not in resource:  # Are we querying a resource (eg: www.ex.com/foo/bar)
        with suppress(NotADatabase):
            if not current_app.auth.has_full_db_access():
                read_perm = lambda p: p == {'account': AccountDomain.actual['_id'], 'perm': READ}
                if resource_name == Account.resource_name or not find(resource.get('perms', []), read_perm):
                    db = AccountDomain.requested_database
                    raise InsufficientDatabasePerm(resource_name, _id=resource['_id'], db=db)
