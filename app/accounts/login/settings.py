import base64

from flask import request, jsonify

from app.app import app
from app.exceptions import WrongCredentials
from .access_control import crossdomain


@app.route('/login', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
def login():
    """
    Performs a login. We make this out of eve, being totally open.
    :return:
    """
    try:
        account = app.data.driver.db['accounts'].find_one(
            {'email': request.json['email'], 'password': request.json['password']})
        account['token'] = base64.b64encode(
            str.encode(account['token'] + ':'))  # Framework needs ':' at the end before send it to client
        account['_id'] = str(account['_id'])
        return jsonify(account)
    except:
        raise WrongCredentials('There is not an user with the matching username/password')
