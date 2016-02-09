import copy
import json
import logging
from pprint import pprint

import requests
from requests import HTTPError
from requests.auth import AuthBase

from flask import current_app

from app.app import app


class GRDLogger:
    """
        Given an Id, it sends it to GRD.

        Warning: This methods works outside of Flask's application context, in another thread.
    """

    def __init__(self, event_id: str, token: str, debug: bool, requested_database: str, logging: logging.Logger):
        """
        Sends the vent that event_id represents to GRD.
        :param event_id: String version of the ObjectId of an event.
        """
        self.DEBUG = debug
        self.logging = logging
        self.requested_database = requested_database
        response = app.test_client().get(
            '{}/events/{}'.format(requested_database, event_id),
            environ_base={'HTTP_AUTHORIZATION': 'Basic ' + token}
        )
        event = json.loads(response.data.decode())
        if event['@type'] == 'Register':
            self.register(event)
        else:
            if 'devices' in event:  # We send the same event as many times as devices has
                e = copy.deepcopy(event)
                del e['devices']
                for device in event['devices']:
                    e['device'] = device
                    self.generic(e)
            else:
                self.generic(event)

    def register(self, event: dict):
        """
        Sends a Register event to GRD.
        :param event:
        :return:
        """
        url = 'api/devices/register/'
        data = dict(self.sanitize_generic_event(event), **{
            'device': self.sanitize_device(event['device']),  # We stop all the process if no hid
            'components': []
        })
        for component in event['components']:
            try:
                data['components'].add(self.sanitize_device(component))
            except KeyError as e:
                if e.args[0] == 'hid':
                    pass  # We do not send one component without hid, but we do not stop the process
                else:
                    raise e
        self._post(data, url)

    def generic(self, event: dict):
        """
        Sends a regular event (this is, without any special field) to GRD.
        :param event:
        :return:
        """
        data = dict(self.sanitize_generic_event(event))
        url = 'api/devices/{}/{}'.format(data['device'], event['@type'].lower()) # We replaced full device per hid
        self._post(data, url)

    def sanitize_device(self, device: dict) -> dict:
        """
        Removes any data that is not interested for GRD, and transforms other to the format GRD wants it.
        :param device:
        :return: returns a device dictionary with the needed data.
        """
        return {
            'hid': device['hid'],
            'id': str(device['_id']),
            'pid': str(device['pid']),
            'type': device['@type'],
            'url': '{}/devices/{}'.format(self.requested_database, device['_id'])
        }

    def sanitize_generic_event(self, event: dict) -> dict:
        """
        As @see sanitize_device, but with an event.
        :param event:
        :return:
        """
        return {
            'url': '{}/events/{}'.format(self.requested_database, event['_id']),
            'date': str(event['_created']),
            'byUser': 'accounts/{}'.format(event['_id'])  # There is no requested_database for the url of the account
        }

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
            r = requests.post(app.config['GRD_DOMAIN'] + url, json=event, auth=GRDAuth())
            try:
                r.raise_for_status()
            except HTTPError or ConnectionError:
                text = ''
                if r.status_code != 500:
                    text = str(r.json())
                self.logging.error('Error: event {}: {} from url {} \n {}'.format(json.dumps(event), r.status_code,
                                                                                  url, text))
            else:
                self.logging.debug("GRDLogger: Succeed POST event " + json.dumps(event) + ' from url ' + url)

    @staticmethod
    def _post_debug(event: dict, url: str):
        """
        Debug auxiliar function.
        :param event:
        :param url:
        :return:
        """
        pprint("GRDLogger, fake post: event " + json.dumps(event) + ", to url " + url)


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
        account = current_app.config['GRD_ACCOUNT']
        r = requests.post(app.config['GRD_DOMAIN'] + 'api-token-auth/', json=account)
        data = r.json()
        return data['token']
