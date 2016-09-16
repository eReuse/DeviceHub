import requests
from flask import json
from requests import HTTPError

from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.submitter.translator import Translator
from ereuse_devicehub.rest import execute_get
from ereuse_devicehub.security.request_auth import Auth
from ereuse_devicehub.utils import Naming


class Submitter:
    """
        Submits resources to other agents.

        Submitter is thought to be working outside of Flask's application context, in another thread.
    """
    def __init__(self, token: str, app: 'DeviceHub', domain: str, translator: Translator, auth: Auth, debug=False):
        """
        :param token: Token of the Submitter user in DeviceHub.
        :param domain: The destination domain or IP.
        :param translator: A translator instance.
        :param auth: An Auth instance.
        :param debug: If true, data is not actually submitted but locally logged.
        """
        self.config = app.config
        self.domain = domain
        self.translator = translator
        self.debug = debug
        self.auth = auth
        self.token = token
        self.app = app
        self.logger = app.logger
        self.embedded = {'device': 1, 'devices': 1, 'components': 1}

    def submit(self, resource_id: str, database: str, resource_name: str):
        """
        Submits the resource to the configured agent.
        :param resource_id: The identifier (_id) in DeviceHub of the resource.
        :param database: The database or inventory (db1...) to get the resource from.
        :param resource_name: The name of the resource.
        """
        #path = self.config['DOMAIN'][resource_name]['url']
        url = '{}/{}/{}{}'.format(database, 'events', resource_id, '?embedded={}'.format(json.dumps(self.embedded)))
        with self.app.app_context():
            event = execute_get(url, self.token)
        for translated_resource, original_resource in self.translator.translate(database, event):
            submission_url = self.generate_url(original_resource, translated_resource)
            self._post(translated_resource, submission_url)

    def generate_url(self, original_resource, translated_resource) -> str:
        """Generates the url to submit the resource to, in the external agent."""
        raise NotImplementedError()

    def _post(self, resource: dict, url: str, **kwargs):
        """Sends the resource to the agent. Kwargs are sent to Request's Post"""
        if self.debug:
            self.logger.info('GRDLogger: succeed FAKE post event \n{}\n to url {}'.format(json.dumps(resource), url))
        else:
            r = requests.post(url, json=resource, auth=self.auth, **kwargs)
            try:
                r.raise_for_status()
            except HTTPError or ConnectionError:
                text = str(r.json()) if 200 <= r.status_code < 300 else ''
                error = 'Error: event \n{}\n: {} from url {} \n {}'.format(json.dumps(resource), r.status_code, url, text)
                self.logger.error(error)
            else:
                self.logger.info("GRDLogger: Succeed POST event \n{}\n from {}".format(json.dumps(resource), url))
