import copy

from flask import current_app
from flask import json

from ereuse_devicehub.exceptions import SchemaError
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.submitter.grd_submitter.old_translator import ResourceTranslator
from ereuse_devicehub.resources.submitter.submitter import Submitter
from ereuse_devicehub.rest import execute_get
from ereuse_devicehub.utils import Naming


class MigrateSubmitter(Submitter):
    def generate_url(self, original_resource, translated_resource) -> str:
        return '{}{}/events/devices/migrate'.format(original_resource['to']['baseUrl'],
                                                    original_resource['to']['database'])


class MigrateTranslator(ResourceTranslator):
    """
    Translator for Migrate.

    Note that this translator is different from others in the sense that does not use the same translation technique,
    the translation dicts, but a more simpler one, that better fits its situation.
    """

    def _translate(self, resource: dict) -> dict:
        translation = {
            '@type': 'devices:Migrate',
            'from': current_app.config['BASE_URL_FOR_AGENTS'] + '/' + resource['_links']['self']['href'],
            'devices': [self.get_device(device_id) for device_id in resource['devices']]
        }
        if 'label' in resource:
            translation['label'] = resource['label']
        if 'comment' in resource:
            translation['comment'] = resource['comment']
        return translation

    def get_device(self, device_id: str) -> dict:
        """Gets the device ready to be sent to another database."""
        # It is just so easy to load stuff (through permissions, etc) through Python-Eve's API
        embedded = json.dumps({'components': 1})
        projection = json.dumps({'events': 0})
        token = AccountDomain.hash_token(AccountDomain.actual_token)
        url = '{}/devices/{}?embedded={}&projection={}'.format(self.database, device_id, embedded, projection)
        device = execute_get(url, token)
        self.clean_device(device)
        for component in device.get('components', []):
            self.clean_device(component)
        return device

    @staticmethod
    def clean_device(device: dict):
        """Removes values that are not supposed to be sent, like materialized or readonly ones."""
        schema = current_app.config['DOMAIN'][Naming.resource(device['@type'])]['schema']
        _id = device['_id']
        for field in copy.copy(device):
            if '_' in field or not {'materialized', 'readonly'}.isdisjoint(set(schema[field].keys())):
                del device[field]
        device['url'] = DeviceDomain.url_agent_for(AccountDomain.get_requested_database(), _id)


class DeviceHasMigrated(SchemaError):
    def __init__(self, device_id, migrate):
        super().__init__(device_id, json.dumps(migrate))
