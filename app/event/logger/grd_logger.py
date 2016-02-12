import copy
import json
import logging
from pprint import pprint

import requests
from requests import HTTPError
from requests.auth import AuthBase

from flask import current_app

from app.app import app
from app.utils import get_resource_name

NONEXISTENT_EVENTS_IN_GRD = 'snapshot', 'test-hard-drive', 'erase-basic'


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
        if 'components' in event:
            self.register(event)  # It is the only event submitting a full device object
        else:
            if 'devices' in event:
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
        data = dict(self.sanitize_generic_event(event), **{'components': []})
        data['device'] = self.get_full_device(event['device'])
        for component in event['components']:
            data['components'].add(self.get_full_device(component))
        self._post(data, url)

    def generic(self, event: dict):
        """
        Sends a regular event (this is, without any special field) to GRD.
        :param event:
        :return:
        """
        data = dict(self.sanitize_generic_event(event))
        #url = 'api/devices/{}/{}'.format(, get_resource_name(event['@type']))
        url = 'dummy'
        self._post(data, url)

    def get_full_device(self, device: dict) -> dict:
        """
        Gets a device for the GRD. This is, the device object with only the interesting fields for GRD, or an URL
        that acts like a reference.
        :param device:
        :return: returns a device dictionary with the needed data, or an URL.
        """
        grd_device = {
            'id': str(device['_id']),
            'pid': str(device['pid']),
            'type': device['@type'],
            'url': self.get_resource_url(device['_id'], 'devices')
        }
        try:
            grd_device['hid'] = device['hid']
        except KeyError as e:
            if e.args[0] == 'hid':
                return grd_device['url']
            else:
                raise e
        return grd_device

    def sanitize_generic_event(self, event: dict) -> dict:
        """
        As @see sanitize_device, but with an event.
        :param event:
        :return:
        """
        grd_event = {
            'url': self.get_resource_url(event['_id'], 'accounts'),
            'date': event['_created'],
            'byUser': 'accounts/{}'.format(event['byUser']),  # There is no requested_database for the url of the account
            'device': self.get_hid_or_url(event['device'])
        }
        if 'components' in event:
            grd_event['components'] = [self.get_hid_or_url(component) for component in event['components']]
        return grd_event

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

    def get_resource_url(self, identifier, resource):
        return '{}/{}/{}'.format(self.requested_database, resource, identifier)

    def get_hid_or_url(self, device):
        return device.get('hid', self.get_resource_url(device['_id'], 'devices'))


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
