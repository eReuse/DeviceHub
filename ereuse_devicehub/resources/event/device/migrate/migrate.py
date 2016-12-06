import copy

from ereuse_devicehub.exceptions import SchemaError
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.place.domain import PlaceDomain
from ereuse_devicehub.rest import execute_get, execute_post, execute_patch
from ereuse_devicehub.utils import Naming
from flask import current_app
from flask import json
from flask import request

class MigrateSubmit:
    def __init__(self, to, device_ids, url, label, comment):
        self.to = to
        self.device_ids = device_ids
        self.devices = []
        self.url = url
        self.label = label
        self.comment = comment

    def execute(self):
        for device_id in self.device_ids:
            self.devices.append(self.get_device(device_id))
        url = self.submit()
        self.remove_devices_from_places()
        return url

    @classmethod
    def get_device(cls, device_id: str) -> dict:
        """Gets the device ready to be sent to another database"""
        # It is just so easy to load stuff (through permissions, etc) through Python-Eve's API
        embedded = json.dumps({'components': 1})
        projection = json.dumps({'events': 0})
        db = AccountDomain.get_requested_database()
        token = AccountDomain.hash_token(AccountDomain.actual_token)
        url = '{}/devices/{}?embedded={}&projection={}'.format(db, device_id, embedded, projection)
        device = execute_get(url, token)
        cls.clean_device(device)
        for component in device.get('components', []):
            cls.clean_device(component)
        return device

    @staticmethod
    def clean_device(device: dict):
        schema = current_app.config['DOMAIN'][Naming.resource(device['@type'])]['schema']
        for field in copy.copy(device):
            if '_' in field or not {'materialized', 'readonly'}.isdisjoint(set(schema[field].keys())):
                del device[field]

    @staticmethod
    def get_agent_account_token() -> str:
        """
        :return: The hashed token
        """
        # Hardcoded token for machine account
        email, password = current_app.config['AGENT_ACCOUNTS']['self']
        response = execute_post('login', {'@type': 'Account', 'email': email, 'password': password})
        return response['token']

    def submit(self) -> str:
        """
        Submits the migrate.

        :return: str The URL of the destination Migrate.
        """
        migrate = {
            '@type': 'devices:Migrate',
            'from': request.url_root + self.url,
            'devices': self.devices,
            'label': self.label,
            'comment': self.comment
        }

        # todo make this for non-same-devicehub situations
        # In testing situations we may not know our own domain / port (localhost:????)
        headers = [('authorization', 'Basic ' + self.get_agent_account_token())]
        url = '{}/events/devices/migrate'.format(self.to['database'])
        response = execute_post(url, migrate, headers)
        return self.to['baseUrl'] + response['_links']['self']['href']

    def remove_devices_from_places(self):
        """Removes the devices of the migrate from their place"""
        for device in self.devices:
            if 'place' in device:
                place = PlaceDomain.get_one(device['place'])
                devices = set(place['devices'])
                devices.remove(device['_id'])
                execute_patch('places', {'@type': 'Place', 'devices': list(devices)}, place['_id'])


class DeviceHasMigrated(SchemaError):
    def __init__(self, device_id, migrate):
        super().__init__(device_id, json.dumps(migrate))
