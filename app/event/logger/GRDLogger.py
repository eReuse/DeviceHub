from logging import getLogger
from pip._vendor import requests
from pip._vendor.requests import HTTPError

__author__ = 'busta'


class GRDLogger:
    def __init__(self, event: dict):
        if event['@type'] == 'Register':
            self.register(event)
            # todo other events

    def register(self, event: dict):
        # todo remove unnecesary data from event, prepare url...
        url = 'url...'
        self.send(event, url)

    @staticmethod
    def send(event: dict, url: str):
        domain = 'https://..../'
        logger = getLogger()
        r = requests.post(domain + url, json=event)  # todo does event need to be json or requests does it?
        try:
            r.raise_for_status()
        except HTTPError:
            logger.error("GRDLogger: error from GRD for event" + event['_id'] + " of type" +
                         event['@type'] + ": " + r.status_code + r.json())
        else:
            logger.debug("GRDLogger: Succeed POST event " + event['_id'] + " of type" + event['@type'])
