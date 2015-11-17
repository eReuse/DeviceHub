import copy
import json
import logging
from pprint import pprint

import requests
from requests import HTTPError
from requests.auth import AuthBase

from app.app import app


class GRDLogger:
    """
        Given an Id, it sends it to GRD.
    """

    DEBUG = False

    def __init__(self, event_id: str, token: str):
        """
        Sends the vent that event_id represents to GRD.
        :param event_id: String version of the ObjectId of an event.
        """
        response = app.test_client().get('events/' + event_id, environ_base={'HTTP_AUTHORIZATION': 'Basic ' + token})
        event = json.loads(response.data.decode(app.config['ENCODING']))
        try:
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
        except KeyError as e:
            if e.args[0] == 'hid':
                pass  # We do not send to GRD devices without hid
            else:
                raise e


    def register(self, event: dict):
        """
        Sends a Register event to GRD.
        :param event:
        :return:
        """
        url = 'api/devices/register/'
        data = dict(self.sanitize_generic_event(event), **{
            'device': self.sanitize_device(event['device']),
            'components': [self.sanitize_device(component) for component in event['components']]
        })
        self._post(data, url)

    def generic(self, event: dict):
        """
        Sends a regular event (this is, without any special field) to GRD.
        :param event:
        :return:
        """
        data = dict(self.sanitize_generic_event(event), **{
            'device': event['device']['hid']
        })
        url = 'api/devices/' + data['device'] + '/' + event['@type'].lower()  # We replaced full device per hid
        self._post(data, url)

    @classmethod
    def sanitize_device(cls, device: dict) -> dict:
        """
        Removes any data that is not interested for GRD, and transforms other to the format GRD wants it.
        :param device:
        :return: returns a device dictionary with the needed data.
        """
        return {
            'hid': device['hid'],
            'id': str(device['_id']),
            'type': device['@type'],
            'url': app.config['ENCODING'] + 'devices/' + str(device['_id'])
        }

    @classmethod
    def sanitize_generic_event(cls, event: dict) -> dict:
        """
        As @see sanitize_device, but with an event.
        :param event:
        :return:
        """
        return {
            'url': app.config['ENCODING'] + 'events/' + str(event['_id']),
            'date': str(event['_created']),
            'byUser': '1',  # todo we will need to transform the uid to an url
        }

    @classmethod
    def _post(cls, event: dict, url: str):
        """
        Sends an event, performing the post method.
        :param event:
        :param url:
        :return:
        """
        if cls.DEBUG:
            cls._post_debug(event, url)
        else:
            logging.basicConfig(filename="logs/GRDLogger.log", level=logging.INFO)  # Another process, another logger
            r = requests.post(app.config['GRD_DOMAIN'] + url, json=event, auth=GRDAuth())
            try:
                r.raise_for_status()
            except HTTPError or ConnectionError:
                text = ''
                if r.status_code != 500:
                    text = str(r.json())
                logging.error("Error: event " + json.dumps(event) + ": " + str(
                    r.status_code) + ' from url ' + url + '\n' + text)
            else:
                logging.debug("GRDLogger: Succeed POST event " + json.dumps(event) + ' from url ' + url)

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
        json = {"username": "ereuse", "password": "ereuse@grd"}
        r = requests.post(app.config['GRD_DOMAIN'] + 'api-token-auth/', json=json)
        data = r.json()
        return data['token']
