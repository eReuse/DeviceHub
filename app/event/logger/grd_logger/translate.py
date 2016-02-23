import copy
from pprint import pprint
from urllib.parse import quote_plus

from app.app import app
from app.rest import execute_get
from app.utils import get_last_exception_info
from settings import RESOURCES_NOT_USING_CUSTOM_DATABASES, URL_PREFIX

class Translate:
    requested_database = ''
    token = ''

    @staticmethod
    def translate(event, requested_database, token):
        try:
            Translate.requested_database = requested_database  # This value makes Translate not safe for use with parallelism
            Translate.token = token
            translated = []
            if 'devices' in event and event['@type'] != 'Register':
                e = copy.deepcopy(event)
                del e['devices']
                for device in event['devices']:
                    e['device'] = device
                    translated.append((Translate.translate_one(e), copy.deepcopy(e)))
            else:
                translated.append((Translate.translate_one(event), event))
            return translated
        except Exception as e:
            app.logger.error(get_last_exception_info())
            e.ok = True
            raise e

    @staticmethod
    def translate_one(event):
        translated = dict()
        for final_name, (method, *original_name) in dict(GENERIC_EVENT, **TRANSLATION[event['@type']]).items():
            try:
                value = event[original_name[0] if len(original_name) > 0 else final_name]
            except KeyError:
                pass
            else:
                translated[final_name] = method(value)
        return translated

    @staticmethod
    def url(resource):
        def url(identifier):
            return Translate.get_resource_url(identifier, resource)
        return url

    @staticmethod
    def identity(value):
        return value

    @staticmethod
    def get_full_components(components: list) -> list:
        ret = []
        for component in components:
            ret.append(Translate.get_full_device(component))
        return ret

    @staticmethod
    def get_full_device(device: dict) -> dict:
        """
        Gets a device for the GRD. This is, the device object with only the interesting fields for GRD, or an URL
        that acts like a reference.
        :param device:
        :return: returns a device dictionary with the needed data, or an URL.
        """
        grd_device = {
            '@type': device['@type'],
            'url': Translate.get_resource_url(device['_id'], 'devices'),
        }
        if 'pid' in device:
            grd_device['pid'] = device['pid']
        if 'hid' in device:
            grd_device['hid'] = device['hid']
        return grd_device

    @staticmethod
    def get_hid_or_url_loop(devices):
        return [Translate.get_hid_or_url(device) for device in devices]

    @staticmethod
    def get_hid_or_url(device: dict, parse_grd_url=False):
        hid = device.get('hid')
        if not hid:
            url = Translate.get_resource_url(device['_id'], 'devices')
            if parse_grd_url:
                url = Translate.parse_grd_url(url)
            return url
        else:
            return hid

    @staticmethod
    def parse_grd_url(url):
        return quote_plus(url.replace('/', '!'))

    @staticmethod
    def get_resource_url(identifier, resource):
        if resource in RESOURCES_NOT_USING_CUSTOM_DATABASES:
            url = '{}/{}'.format(resource, identifier)
        else:
            url = '{}/{}/{}'.format(Translate.requested_database, resource, identifier)
        return Translate.parse_url(url)

    @staticmethod
    def parse_url(url):
        if URL_PREFIX:
            url = '{}/{}'.format(URL_PREFIX, url)
        return app.config['BASE_PATH_SHOWN_TO_GRD'] + url


"""
The properties used for all the events. Note that GRD does not need '@type' for the main resource
"""
GENERIC_EVENT = {
    'url': (Translate.url('events'), '_id'),
    'date': (Translate.identity,),
    'byUser': (Translate.url('accounts'),),
    'dhDate': (Translate.identity, '_created'),
    'errors': (Translate.identity, '_errors'),
    'secured': (Translate.identity,),
    'incidence': (Translate.identity,),
    'device': (Translate.get_hid_or_url,),
    'geo': (Translate.identity,),
    '@type': (Translate.identity,)
}

TRANSLATION = {
    'Register': {
        'offline': (Translate.identity,),
        'device': (Translate.get_full_device,),
        'components': (Translate.get_full_components,)
    },
    'Deallocate': {
        'from': (Translate.url('accounts'),)
    },
    'Allocate': {
        'to': (Translate.url('accounts'),)
    },
    'UsageProof': {
        'softwareVersion': (Translate.identity,)
    },
    'Receive': {
        'receiver': (Translate.url('accounts'),),
        'type': (Translate.identity,),
        'place': (Translate.url('places'),)
    },
    'Add': {
        'components': (Translate.get_hid_or_url_loop,)
    },
    'Remove': {
        'components': (Translate.get_hid_or_url_loop,)
    },
    'Locate': {
        'place': (Translate.url('places'),)
    },
    'Recycle': dict(),
    'Migrate': dict()
}

