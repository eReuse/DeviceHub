import requests
from flask import current_app
from requests.auth import AuthBase


class Auth(AuthBase):
    """
    Handles the authorization method.

    If there is no available token for us, it logs-in and stores the token. Appends the token to the header accordingly.
    """

    def __init__(self, domain: str, email: str, password: str, login_path: str = 'login', auth_header_title='Basic'):
        self.domain = domain
        self.email = email
        self.password = password
        self.token = None
        self.login_path = login_path
        self.auth_header_title = auth_header_title

    def __call__(self, r):
        if self.token is None:
            self.token = self.login()
        r.headers['Authorization'] = '{} {}'.format(self.auth_header_title, self.token)
        return r

    def login(self):
        account = {
            'email': self.email,
            'password': self.password
        }
        r = requests.post('{}/{}'.format(self.domain, self.login_path), json=account)
        data = r.json()
        return data['token']


class AgentAuth(Auth):
    """
        Handles Authorization for Agents which credentials are stored in the 'BASE_URL_FOR_AGENTS' config dict.

        The 'BASE_URL_FOR_AGENTS' is a dict with the following structure:

            { base_url|'self': (email_of_agent_account, password_of_agent_account)}

        Like in the following example:

            {'self': ('self@ereuse.org', '12345'), 'https://example.com': ('mail@mail.com', '123')}

        Note that 'self' is a reserved keyword that is interpreted as the own DeviceHub.
    """
    def __init__(self, base_url: str, **kwargs):
        if current_app.config['BASE_URL_FOR_AGENTS'] in base_url:
            base_url = 'self'
        # To use this in another thread we should remove 'current_app' and get the configuration file through
        # another way
        email, password = current_app.config['AGENT_ACCOUNTS'][base_url]
        login_path = kwargs.get('login_path', 'login')
        auth_header_title = kwargs.get('auth_header_title', 'Basic')
        super().__init__(base_url, email, password, login_path, auth_header_title)
