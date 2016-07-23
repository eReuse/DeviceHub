from flask import current_app

from ereuse_devicehub.security.request_auth import Auth


class GRDAuth(Auth):
    """
    Handles the authorization method GRD needs. This is token at django style.

    If there is no available token for us, it logs-in and stores the token. Appends the token to the header accordingly.
    """
    token = None
    AUTH_HEADER_TITLE = 'Token'

    # noinspection PyMissingConstructor
    def __init__(self):
        self.domain = current_app.config['GRD_DOMAIN']
        account = current_app.config['GRD_ACCOUNT']
        self.email = account['email']
        self.password = account['password']
        self.login_path = 'api-token-auth/'
