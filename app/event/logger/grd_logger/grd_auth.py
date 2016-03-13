from app.security.request_auth import Auth
from settings import GRD_DOMAIN, GRD_ACCOUNT


class GRDAuth(Auth):
    """
    Handles the authorization method GRD needs. This is token at django style.

    If there is no available token for us, it logs-in and stores the token. Appends the token to the header accordingly.
    """
    token = None
    AUTH_HEADER_TITLE = 'Token'

    # noinspection PyMissingConstructor
    def __init__(self):
        self.domain = GRD_DOMAIN
        self.email = GRD_ACCOUNT['email']
        self.password = GRD_ACCOUNT['password']
        self.login_path = 'api-token-auth/'
