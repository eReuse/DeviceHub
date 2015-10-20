import json
from logging import getLogger
from pprint import pprint

from pip._vendor import requests
from pip._vendor.requests import HTTPError
from pip._vendor.requests.auth import AuthBase

__author__ = 'busta'

DOMAIN = 'https://sandbox.ereuse.org/'


class GRDLogger:
    OWN_DOMAIN = 'https://devicehub.ereuse.org/'
    DEBUG = False

    def __init__(self, event: dict):
        if event['@type'] == 'Register':
            self.register(event)
        else:
            self.generic(event)

    def register(self, event: dict):
        url = 'api/devices/register/'
        data = dict(self.sanitize_generic_event(event), **{
            'device': self.sanitize_device(event['device']),
            'components': [self.sanitize_device(component) for component in event['components']]
        })
        self._post(data, url)

    def generic(self, event: dict):
        data = dict(self.sanitize_generic_event(event), **{
            'device': event['device']  # We get hid
        })
        url = 'api/devices/' + data['device']['hid'] + '/' + event['@type'].lower()
        self._post(data, url)

    @classmethod
    def sanitize_device(cls, device: dict):
        return {
            'hid': device['hid'],
            'id': str(device['_id']),
            'type': device['@type'],
            'url': cls.OWN_DOMAIN + 'devices/' + str(device['_id'])
        }

    @classmethod
    def sanitize_generic_event(cls, event: dict):
        return {
            'url': cls.OWN_DOMAIN + 'events/' + str(event['_id']),
            'date': str(event['_created']),
            'byUser': '1',  # todo we will need to transform the uid to an url
        }

    @classmethod
    def _post(cls, event: dict, url: str):
        if cls.DEBUG:
            cls._post_debug(event, url)
        else:
            logger = getLogger('DeviceHub')
            r = requests.post(DOMAIN + url, json=event,
                              auth=GRDAuth())  # todo does event need to be json or requests does it?
            try:
                r.raise_for_status()
            except HTTPError:
                logger.error("GRDLogger, error: event " + json.dumps(event) + ": " + str(r.status_code) + ' from url ' + url + '\n' + r)
            except ConnectionError:
                logger.error("GRDLogger, error: event " + json.dumps(event) + ', ' + str(r.status_code) + ' from url ' + url + '\n' + r)
            else:
                logger.debug("GRDLogger: Succeed POST event " + json.dumps(event) + ' from url ' + url)

    @staticmethod
    def _post_debug(event: dict, url: str):
        pprint("GRDLogger, fake post: event " + json.dumps(event) + ", to url " + url)


class GRDAuth(AuthBase):
    token = None  # Class attribute todo know when is going to expire

    def __call__(self, r):
        if self.token is None:
            self.token = self.login()
        r.headers['Authorization'] = 'Token ' + self.token
        return r

    @staticmethod
    def login():
        json = {"username": "ereuse", "password": "ereuse@grd"}
        r = requests.post(DOMAIN + 'api-token-auth/', json=json)
        data = r.json()
        return data['token']

