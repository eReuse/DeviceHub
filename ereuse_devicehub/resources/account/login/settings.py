from flask import request, jsonify

from ereuse_devicehub.exceptions import WrongCredentials
from ereuse_devicehub.resources.account.domain import AccountDomain, UserNotFound


def login():
    """
    Performs a login. We make this out of eve, being totally open.
    :return:
    """
    try:
        json = request.get_json()
        account = AccountDomain.get_one({'email': json['email']})
        if not AccountDomain.verify_password(json['password'], account['password']):
            raise WrongCredentials()
        del account['password']
        account['token'] = AccountDomain.hash_token(account['token'])
        account['_id'] = str(account['_id'])
        return jsonify(account)
    except (KeyError, TypeError, UserNotFound) as e:
        raise WrongCredentials() from e
