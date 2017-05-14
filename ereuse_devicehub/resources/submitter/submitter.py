import requests
from flask import json
from requests import HTTPError
from werkzeug.urls import url_parse, URL, url_unparse

from ereuse_devicehub.resources.submitter.grd_submitter.old_translator import ResourceTranslator
from ereuse_devicehub.rest import execute_get, execute_post
from ereuse_devicehub.security.request_auth import Auth


class Submitter:
    """
    Submitter class.

    Prepares (translates) a resource to fit another agent's API and submits to it.
    """

    def __init__(self, app: 'DeviceHub', translator: ResourceTranslator = None, auth: Auth = None, debug=False,
                 **kwargs):
        self.auth = auth
        self.app = app
        self.config = app.config
        self.logger = app.logger
        self.translator = translator
        self.debug = self.config['DEBUG'] if debug is None else debug

    def submit(self, original_resource: dict, database: str):
        responses = []
        for translated_resource, original_resource in self.translator.translate(original_resource, database):
            submission_url = self.generate_url(original_resource, translated_resource)
            responses.append(self._post(translated_resource, submission_url))
        return responses

    def _post(self, translated_resource: dict, url: str, **kwargs):
        """Sends the resource to an agent or itself"""
        if self.config['BASE_URL_FOR_AGENTS'] in url:  # We submit the resource to ourselves
            url = url_parse(url)  # We need to remove the base path
            absolute_path_ref = url_unparse(URL('', '', url.path, url.query, url.fragment))
            response = self._post_internal(translated_resource, absolute_path_ref)
        else:
            response = self._post_external(translated_resource, url, **kwargs)
        return response

    def _post_external(self, translated_resource: dict, url: str, **kwargs):
        """Sends the resource to an external agent. Kwargs are sent to Request's Post"""
        if self.debug:
            self.logger.info('Submitter: OK FAKE POST \n{}\n to url {}'.format(json.dumps(translated_resource), url))
        else:
            r = requests.post(url, json=translated_resource, auth=self.auth, **kwargs)
            try:
                r.raise_for_status()
            except HTTPError or ConnectionError:
                text = str(r.json()) if 200 <= r.status_code < 300 else ''
                error = 'Error: event \n{}\n: {} from url {} \n {}'.format(json.dumps(translated_resource),
                                                                           r.status_code, url, text)
                self.logger.error(error)
            else:
                self.logger.info("Submitter: OK FAKE POST \n{}\n from {}".format(json.dumps(translated_resource), url))
                return r

    def _post_internal(self, resource: dict, absolute_path_ref: str):
        """
        Performs POST to the own agent.

        There are two advantages over _post_external:
        a) there is no need to know the actual base-url for the agent (interesting for testing)
        b) it is more efficient

        :param absolute_path_ref: The absolute-path reference of the URI,
            `ref <https://tools.ietf.org/html/rfc3986#section-4.2>`_.
        :return:
        """
        email, password = self.config['AGENT_ACCOUNTS']['self']
        response = execute_post('login', {'@type': 'Account', 'email': email, 'password': password})
        headers = [('authorization', 'Basic ' + response['token'])]
        return execute_post(absolute_path_ref, resource, headers)

    def generate_url(self, original_resource, translated_resource) -> str:
        """Generates the url to submit the resource to, in the external agent."""
        raise NotImplementedError()


class ThreadedSubmitter(Submitter):
    """
        Submits resources to other agents.

        This Submitter is thought to be working outside of Flask's application context, in another thread, so augments
        submit with a way to retreive
    """

    def __init__(self, app: 'DeviceHub', translator: ResourceTranslator = None, auth: Auth = None, debug=False,
                 domain=None,
                 token=None, **kwargs):
        """
        :param translator: A translator instance.
        :param auth: An Auth instance.
        :param debug: If true, data is not actually submitted but locally logged.
        """
        self.domain = domain
        self.token = token
        self.embedded = {'device': 1, 'devices': 1, 'components': 1}
        super().__init__(app, translator, auth, debug, **kwargs)

    def submit(self, resource_id: str, database: str or None, resource_name: str = 'events'):
        """
        Submits the resource to the configured agent.
        :param resource_id: The identifier (_id) in DeviceHub of the resource.
        :param database: The database or inventory (db1...) to get the resource from.
        :param resource_name: The name of the resource.
        """
        url = '{}/{}/{}{}'.format(database, resource_name, resource_id,
                                  '?embedded={}'.format(json.dumps(self.embedded)))
        with self.app.app_context():
            resource = execute_get(url, self.token)
        super().submit(resource, database)

    def generate_url(self, original_resource, translated_resource) -> str:
        raise NotImplementedError()
