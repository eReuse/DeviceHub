import json
from pprint import pprint
from urllib.parse import quote_plus

import requests
from requests import HTTPError
from requests.auth import AuthBase

from app.app import app
from app.rest import execute_get
from app.utils import get_resource_name, get_last_exception_info
from .translate import Translate


class GRDLogger:
    DEBUG = app.config.get('GRD_DEBUG', False)

    """
        Given an Id, it sends it to GRD.

        Warning: This methods works outside of Flask's application context, in another thread.
    """

    def __init__(self, event_id: str, event_type: str, token: str, requested_database: str):
        """
        Sends the vent that event_id represents to GRD.
        :param event_id: String version of the ObjectId of an event.
        """

        try:
            embedded = {}
            if event_type != 'Register':
                embedded = {'device': 1, 'devices': 1, 'components': 1}
            event = execute_get('{}/events/{}{}'.format(requested_database, event_id, '?embedded={}'.format(json.dumps(embedded))), token)
            if event_type == 'Register':
                # 'Components' and 'device' in Register do not act well with embedded
                # as in the schema they are not set with data_relation as they have a double type
                event['components'] = [self.get_device(component_id, requested_database, token) for component_id in event['components']]
                event['device'] = self.get_device(event['device'], requested_database, token)

            for translated_event, original_event in Translate.translate(event, requested_database, token):
                device_identifier = Translate.get_hid_or_url(original_event['device'], True)
                url = self.generate_url(device_identifier, translated_event['@type'])
                self._post(translated_event, url)
        except Exception as e:
            if not hasattr(e, 'ok'):
                app.logger.error(get_last_exception_info())
            raise e

    @staticmethod
    def generate_url(device_identifier, event_type):
        return app.config['GRD_DOMAIN'] + 'api/devices/{}/{}'.format(device_identifier, get_resource_name(event_type))

    @staticmethod
    def get_device(device_id, requested_database, token):
        return execute_get('{}/devices/{}'.format(requested_database, device_id), token)


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
                app.logger.error('Error: event \n{}\n: {} from url {} \n {}'.format(json.dumps(event), r.status_code,
                                                                                    url, text))
            else:
                app.logger.info("GRDLogger: Succeed POST event \n{}\n from {}".format(json.dumps(event), url))

    @staticmethod
    def _post_debug(event: dict, url: str):
        """
        Debug auxiliar function.
        :param event:
        :param url:
        :return:
        """
        app.logger.info('GRDLogger, fake post event \n{}\n to url {}'.format(json.dumps(event), url))


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
