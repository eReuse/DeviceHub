from flask import request, jsonify
from passlib.handlers.sha2_crypt import sha256_crypt

from ereuse_devicehub.exceptions import WrongCredentials
from ereuse_devicehub.flask_decorators import crossdomain
from ereuse_devicehub.resources.account.domain import AccountDomain, UserNotFound


@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
def login():
    """
    Performs a login. We make this out of eve, being totally open.
    :return:
    """
    try:
        account = AccountDomain.get_one({'email': request.json['email']})
        if not sha256_crypt.verify(request.json['password'], account['password']):
            raise WrongCredentials()
        account['token'] = AccountDomain.hash_token(account['token'])
        account['_id'] = str(account['_id'])
        return jsonify(account)
    except (KeyError, TypeError, UserNotFound):
        raise WrongCredentials()
