from ereuse_devicehub.utils import get_last_exception_info


class Translator:
    def __init__(self, token, logger, config, generic_resource: dict, translation_dict: dict):
        self.logger = logger
        self.config = config
        self.token = token
        self.generic = generic_resource
        self.dictionary = translation_dict
        self.database = None

    def translate(self, database: str, resource: dict) -> list:
        """
        Translates a resource.
        :param database: The database in DeviceHub (i.e. db1)
        :param resource: The resource to translate
        :return: A list of tuples, containing 1. the translated resource, 2. the original resource
        """
        self.database = database
        translated = []
        try:
            translated.append((self._translate(resource), resource))
        except Exception as e:
            self.logger.error(get_last_exception_info())
            e.ok = True
            raise e
        else:
            return translated

    def _translate(self, resource: dict) -> dict:
        """
        Translates a resource. This method carries the actual translation.
        :param resource:
        :return: The translated resource
        """
        translated = dict()
        for final_name, (method, *original_name) in dict(self.generic, **self.dictionary[resource['@type']]).items():
            value = resource.get(original_name[0] if len(original_name) > 0 else final_name)
            if value:
                translated[final_name] = method(value)
        return translated

    # Transformers
    def url(self, resource_name: str):
        """Obtains an url from the resource identifier.
        :param resource_name: full resource-name with the prefix, if needed it.
        """
        def url(identifier):
            return self._get_resource_url(identifier, resource_name)
        return url

    def for_all(self, method):
        """Executes a transformer method for each value and returns a list of results"""
        def _loop(values: list) -> list:
            return [method(value) for value in values]
        return _loop

    def identity(self, value):
        """Returns the same value."""
        return value

    def device(self, device: dict) -> dict:
        """Obtains the device"""
        return device

    def hid_or_url(self, device: dict):
        """Returns HID if exists, or the URL of the device otherwise."""
        return device.get('hid', self._get_resource_url(device['_id'], 'devices'))

    # Helpers
    def _get_resource_url(self, identifier, resource_name: str):
        if self.config['DOMAIN'][resource_name]['use_default_database']:
            url = '{}/{}'.format(resource_name, identifier)
        else:
            url = '{}/{}/{}'.format(self.database, resource_name, identifier)
        return self._parse_url(url)

    def _parse_url(self, url):
        if self.config['URL_PREFIX']:
            url = '{}/{}'.format(self.config['URL_PREFIX'], url)
        return self.config['BASE_PATH_SHOWN_TO_GRD'] + '/' + url
