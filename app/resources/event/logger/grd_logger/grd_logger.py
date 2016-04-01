import json

import requests
from requests import HTTPError

from app.app import app
from app.resources.event.logger.grd_logger.grd_auth import GRDAuth
from app.rest import execute_get
from app.utils import Naming, get_last_exception_info
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
            embedded = {'device': 1, 'devices': 1, 'components': 1}
            event = execute_get('{}/events/{}{}'.format(requested_database, event_id, '?embedded={}'.format(json.dumps(embedded))), token)

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
        url = app.config['GRD_DOMAIN']
        if event_type == 'Register':
            url += 'api/devices/register/'
        else:
            url += 'api/devices/{}/{}'.format(device_identifier, Naming.resource(event_type))
        return url

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
                if 200 <= r.status_code < 300:
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



