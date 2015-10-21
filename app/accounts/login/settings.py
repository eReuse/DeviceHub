import base64
from flask import request, jsonify
from app.app import app
from app.exceptions import WrongCredentials

__author__ = 'busta'

@app.route('/login', methods=['POST'])
def login():
    """
    Performs a login. We make this out of eve, being totally open.
    :return:
    """
    try:
        account = app.data.driver.db['accounts'].find_one({'username': request.json['username'], 'password': request.json['password']})
        return jsonify({'token': base64.b64encode(str.encode(account['token'] + ':'))})  # Framework needs ':' at the end before send it to client
    except:
        raise WrongCredentials('There is not an user with the matching username/password')
