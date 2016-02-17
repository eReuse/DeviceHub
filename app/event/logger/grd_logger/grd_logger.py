import json

import requests
from requests import HTTPError
from requests.auth import AuthBase

from app.utils import get_resource_name
from .translate import Translate

from app.app import app


class GRDLogger:
    DEBUG = app.config.get('GRD_DEBUG', False)

    """
        Given an Id, it sends it to GRD.

        Warning: This methods works outside of Flask's application context, in another thread.
    """
    def __init__(self, event_id: str, token: str, requested_database: str):
        """
        Sends the vent that event_id represents to GRD.
        :param event_id: String version of the ObjectId of an event.
        """

        response = app.test_client().get(
            '{}/events/{}'.format(requested_database, event_id),
            environ_base={'HTTP_AUTHORIZATION': 'Basic ' + token}
        )
        event = json.loads(response.data.decode())
        for translated_event in Translate.translate(event, requested_database):
            url = self.generate_url(translated_event['device'], translated_event['@type'])
            del translated_event['device']
            self._post(translated_event, url)

    @staticmethod
    def generate_url(device_identifier, event_type):
        return app.config['GRD_DOMAIN'] + 'api/devices/{}/{}'.format(device_identifier, get_resource_name(event_type))

    def _post(self, event: dict, url: str):
        """
        Sends an event, performing the post method.
        :param event:
        :param url:
        :return:
        """
        if self.DEBUG:
            self._post_debug(event, url)
        else:
            r = requests.post(url, json=event, auth=GRDAuth())
            try:
                r.raise_for_status()
            except HTTPError or ConnectionError:
                text = ''
                if r.status_code != 500:
                    text = str(r.json())
                app.logger.error('Error: event {}: {} from url {} \n {}'.format(event, r.status_code,
                                                                                url, text))
            else:
                app.logger.info("GRDLogger: Succeed POST event {} from {}".format(event, url))

    @staticmethod
    def _post_debug(event: dict, url: str):
        """
        Debug auxiliar function.
        :param event:
        :param url:
        :return:
        """
        app.logger.info('GRDLogger, fake post: event {} to url {}'.format(event, url))


class GRDAuth(AuthBase):
    """
    Handles the authorization method GRD needs. This is token at django style.

    If there is no available token for us, it logs-in and stores the token. Appends the token to the header accordingly.
    """
    token = None  # Class attribute todo know when it is going to expire

    def __call__(self, r):
        if self.token is None:
            self.token = self.login()
        r.headers['Authorization'] = 'Token ' + self.token
        return r

    @staticmethod
    def login():
        account = app.config['GRD_ACCOUNT']
        r = requests.post(app.config['GRD_DOMAIN'] + 'api-token-auth/', json=account)
        data = r.json()
        return data['token']
