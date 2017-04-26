"""
    Submits events to GRD, handling authentication and translation.
"""
import copy
import re
from urllib.parse import quote_plus

from ereuse_devicehub.resources.device.settings import HID_REGEX
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.submitter.submitter import ThreadedSubmitter
from ereuse_devicehub.resources.submitter.translator import ResourceTranslator
from ereuse_devicehub.security.request_auth import Auth
from ereuse_devicehub.utils import Naming


class GRDSubmitter(ThreadedSubmitter):
    def __init__(self, app: 'DeviceHub', translator: ResourceTranslator = None, auth: Auth = None, debug=False,
                 domain=None, token=None, **kwargs):
        config = app.config
        domain = domain or config['GRD_DOMAIN']
        translator = translator or GRDTranslator(config)
        account = config['GRD_ACCOUNT']
        auth = auth or Auth(domain, account['username'], account['password'], 'api-token-auth/', 'Token')
        debug = debug if debug is not None else config.get('GRD_DEBUG', False)
        super().__init__(app, translator, auth, debug, domain, token, **kwargs)

    def generate_url(self, original_resource, translated_resource):
        device_identifier = self.translator.hid_or_url(original_resource['device'])
        if not re.compile(HID_REGEX).match(device_identifier):  # It is not a HID, so it is an URL
            device_identifier = quote_plus(device_identifier.replace('/', '!'))  # Adapt it to GRD needs
        url = self.domain + '/api/devices/'
        event_type = translated_resource['@type']
        if event_type == DeviceEventDomain.new_type('Register'):
            url += 'register'
        else:
            url += '{}/{}'.format(device_identifier, Naming.resource(event_type))
        return url


class GRDTranslator(ResourceTranslator):
    def __init__(self, config):
        generic_resource = {
            'url': (self.url('events'), '_id'),
            'date': (self.identity,),
            'byUser': (self.url('accounts'),),
            'dhDate': (self.identity, '_created'),
            'errors': (self.identity, '_errors'),
            'secured': (self.identity,),
            'incidence': (self.identity,),
            'device': (self.hid_or_url,),
            'geo': (self.identity,),
            '@type': (self.identity,)
        }
        prefix = DeviceEventDomain.new_type
        translation_dict = {
            prefix('Register'): {
                'offline': (self.identity,),
                'device': (self.device,),
                'components': (self.for_all(self.device),)
            },
            prefix('Deallocate'): {
                'from': (self.url('accounts'),)
            },
            prefix('Allocate'): {
                'to': (self.url('accounts'),)
            },
            prefix('UsageProof'): {
                'softwareVersion': (self.identity,)
            },
            prefix('Receive'): {
                'receiver': (self.url('accounts'),),
                'type': (self.identity,),
                'place': (self.url('places'),)
            },
            prefix('Add'): {
                'components': (self.for_all(self.hid_or_url),)
            },
            prefix('Remove'): {
                'components': (self.for_all(self.hid_or_url),)
            },
            prefix('Locate'): {
                'place': (self.url('places'),)
            },
            prefix('Recycle'): dict(),
            prefix('Migrate'): dict()
        }
        super().__init__(config, generic_resource, translation_dict)

    def translate(self, resource: dict, database: str = None) -> list:
        self.database = database
        translated = []
        if resource.get('devices', None) and resource['@type'] != DeviceEventDomain.new_type('Register'):
            e = copy.deepcopy(resource)
            del e['devices']
            for device in resource['devices']:
                e['device'] = device
                translated.append((self._translate(e), copy.deepcopy(e)))
        else:
            translated.append((self._translate(resource), resource))
        return translated

    def device(self, device: dict) -> dict:
        grd_device = {
            '@type': device['@type'],
            'url': self._get_resource_url(device['_id'], 'devices'),
        }
        if 'pid' in device:
            grd_device['pid'] = device['pid']
        if 'hid' in device:
            grd_device['hid'] = device['hid']
        return super().device(grd_device)
