class Translator:
    """
        Translates (or transforms) the structure of a resource to adequate it to another agent.

        Translation is done by specifying a translation dictionary, which is used to change from
        an original resource to the final one.
        Every field of the translation dict contains a method used to transform the original value from
        DeviceHub to the final one. Translator comes with some transformers, and subclass it to add more.

        Translation dictionaries are as follows:
        For generic translation dict: ['final_field_name'] = (transformer_method, 'original field name')
        For specific translation dicts: ['resource type name']['final field name'] = (transformer_method, 'original field name')
        Where 'final field name' is the name of the field in the agent, 'original field name' is the field name
        in DeviceHub (only add it if final name and original name differ), transformer_method is one of the transformer
        methods in Translator, and 'resource type name' e.g. devices:Register.
        See :func `GRDTranslator.__init__`: for an example.
    """
    def __init__(self, config, generic_resource: dict, translation_dict: dict):
        """
        Configures the translator. Once done, you can translate many resources as you want with :func `translate`:.
        :param config:
        :param generic_resource: Generic translation dictionary shared among resources.
        :param translation_dict: Specific translation dictionary divided per resource.
        """
        self.config = config
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
        return [(self._translate(resource), resource)]

    def _translate(self, resource: dict) -> dict:
        """
        Translates a resource. This method carries the actual translation.
        :param resource:
        :return: The translated resource
        """
        translated = dict()
        for final_name, (method, *original_name) in dict(self.generic, **self.dictionary[resource['@type']]).items():
            value = resource.get(original_name[0] if len(original_name) > 0 else final_name)
            if value is not None:
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
