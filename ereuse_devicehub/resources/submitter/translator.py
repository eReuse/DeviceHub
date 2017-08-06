from collections import Iterator

from pydash import map_values, py_


class Translator:
    """
    Base class to translate a resource. Extend this class to have a similar interface, overriding translate and
    translate_one for more specific methods.
    """

    def __init__(self, dictionary: dict):
        """
        Sets the translation dictionary.
        :param dictionary: A translation dictionary whose keys represent the final translated keys and its values
        are a transformation function; a function that called passing by the resource produces the final value for
        the specific field.
        """
        self._translate_many = py_().map(lambda r: self.translate_one(r)).compact()
        self.dict = dictionary

    def translate(self, resources: Iterator) -> list:
        """
        Translates many resources.
        @:return A list of translated resources.
        """
        return self._translate_many(resources)

    def translate_one(self, resource: dict) -> dict:
        """
        Translates a single resource.
        :return: A translated resource.
        """
        return map_values(self.dict, lambda key: key(resource))
