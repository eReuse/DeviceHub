import base64

from flask import request, jsonify
from passlib.handlers.sha2_crypt import sha256_crypt

from app.account.user import User
from app.app import app
from app.exceptions import WrongCredentials
from app.flask_decorators import crossdomain


@app.route('/login', methods=['POST', 'OPTIONS'])
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
        account['token'] = base64.b64encode(
            str.encode(account['token'] + ':'))  # Framework needs ':' at the end before send it to client
        account['_id'] = str(account['_id'])
        return jsonify(account)
    except (KeyError, TypeError):
        raise WrongCredentials()
