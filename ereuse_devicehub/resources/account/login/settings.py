import base64

from flask import request, jsonify
from passlib.handlers.sha2_crypt import sha256_crypt

from ereuse_devicehub.exceptions import WrongCredentials
from ereuse_devicehub.flask_decorators import crossdomain
from ereuse_devicehub.resources.account.user import User


@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
def login():
    """
    Performs a login. We make this out of eve, being totally open.
    :return:
    """
    try:
        account = User.get({'email': request.json['email']})
        if not sha256_crypt.verify(request.json['password'], account['password']):
            raise WrongCredentials()
        account['token'] = User.hash_token(account['token'])
        account['_id'] = str(account['_id'])
        return jsonify(account)
    except (KeyError, TypeError):
        raise WrongCredentials()
