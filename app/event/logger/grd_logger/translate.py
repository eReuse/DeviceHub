import copy

from settings import RESOURCES_NOT_USING_CUSTOM_DATABASES, URL_PREFIX

from app.app import app

class Translate:
    requested_database = ''

    @staticmethod
    def translate(event, requested_database):
        Translate.requested_database = requested_database  # This value makes Translate not safe for use with parallelism
        translated = []
        if 'devices' in event and event['@type'] != 'Register':
            e = copy.deepcopy(event)
            del e['devices']
            for device in event['devices']:
                e['device'] = device
                translated.append(Translate.translate_one(e))
        else:
            translated.append(Translate.translate_one(event))
        return translated

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
            'id': str(device['_id']),
            '@type': device['@type'],
            'url': Translate.get_resource_url(device['_id'], 'devices'),
        }
        if 'pid' in device:
            grd_device['pid'] = device['pid']
        try:
            grd_device['hid'] = device['hid']
        except KeyError as e:
            if e.args[0] == 'hid':
                return grd_device['url']
            else:
                raise e
        return grd_device

    @staticmethod
    def get_hid_or_url_loop(devices):
        return [Translate.get_hid_or_url(device) for device in devices]

    @staticmethod
    def get_hid_or_url(device):
        return device.get('hid', Translate.get_resource_url(device['_id'], 'devices'))

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
        url = app.config['BASE_PATH_SHOWN_TO_GRD'] + url
        return url.replace('/', '!')


GENERIC_EVENT = {
    'url': (Translate.url('events'), '_id'),
    'date': (Translate.identity,),
    'byUser': (Translate.url('byUser'), 'accounts'),
    'dhDate': (Translate.identity, '_created'),
    'errors': (Translate.identity, '_errors'),
    'secured': (Translate.identity,),
    'incidence': (Translate.identity,),
    'device': (Translate.get_hid_or_url,),
    'geo': (Translate.identity,),
    '@type': (Translate.identity,),
}

TRANSLATION = {
    'Register': {
        'offline': (Translate.identity,),
        'device': (Translate.get_full_device,),
        'components': (Translate.get_full_components,)
    },
    'Deallocate': {
        'to': (Translate.url('accounts'),)
    },
    'Allocate': {
        'from': (Translate.url('accounts'),)
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
