import validators
from bson import ObjectId
from flask import current_app

from ereuse_devicehub.exceptions import SchemaError


class Coercer:
    """Contains general 'coerces' used by validation"""

    @staticmethod
    def url_to_id(url, field_name, document, schema):
        """
        Given an URL, looks for a resource with the same URL in the sameAs field. If succeeds, returns the internal id,
        otherwise throws error. If the value is not an URL it only returns the value.
        :param url:
        :param field_name:
        :param document:
        :return: the internal (DeviceHub) identifier of the resource. Note that ObjectId are parsed to str to mimic JSON.
        """
        if validators.url(str(url)):
            data_relation = schema[field_name]['data_relation']
            response = current_app.data.find_one_raw(data_relation['resource'], {'sameAs': {'$in': [url]}})
            if response is not None:
                return response[data_relation['field']]
            else:
                raise SchemaError('There is no {} with the field {} "{}".'.format(data_relation['resource'], field_name,
                                                                                  url))
        else:
            return url
