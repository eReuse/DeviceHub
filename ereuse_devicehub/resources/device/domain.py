from eve.utils import document_etag
from flask import current_app
from passlib.utils import classproperty

from ereuse_devicehub.resources.device.exceptions import DeviceNotFound
from ereuse_devicehub.resources.device.settings import DeviceSettings
from ereuse_devicehub.resources.domain import Domain, ResourceNotFound
from ereuse_devicehub.utils import Naming


class DeviceDomain(Domain):
    resource_settings = DeviceSettings

    @classmethod
    def get_one(cls, id_or_filter: str or dict) -> dict:
        """
        :throws DeviceNotFound:
        """
        try:
            return super().get_one(id_or_filter)
        except ResourceNotFound as e:
            raise DeviceNotFound(e.message) from e

    @staticmethod
    def generate_etag(device: dict) -> str:
        domain = current_app.config['DOMAIN']
        return document_etag(device, domain[Naming.resource(device['@type'])]['etag_ignore_fields'])

    @classmethod
    def seem_equal(cls, x: dict, y: dict) -> bool:
        x_tag = x['_etag'] if '_etag' in x else cls.generate_etag(x)
        y_tag = y['_etag'] if '_etag' in y else cls.generate_etag(y)
        return x_tag == y_tag

    @classmethod
    def difference(cls, list_to_remove_devices_from, checking_list):
        """
        Computes the difference between two lists of devices.

        To compute the difference the position of the parameters is important
        :param list_to_remove_devices_from:
        :param checking_list:
        :return:
        """
        difference = []
        for x in list_to_remove_devices_from:
            for y in checking_list:
                if cls.seem_equal(x, y):
                    break
            else:
                difference.append(x)
        return difference

    @classproperty
    def uid_fields(cls):
        """Returns the fields that are uids."""
        return {name for name, field in cls.resource_settings._schema.actual_fields().items() if 'uid' in field}

    @classproperty
    def external_synthetic_ids(cls):
        """
        Return fields that are external synthetic ids.

        As for The National Institute of Standards and Technology (NIST) from the United States,
        Synthetic identifiers “are meant to be used when a database or process assigns an identifier”,
        which are the identifiers’ organizations and systems assigned to devices when they are introduced to them.

        External ids are the ones not internally set by DeviceHub (the _id), as we do not usually want to treat
        _id as other external synthetic ids.
        """
        return {n for n, field in cls.resource_settings._schema.actual_fields().items() if 'externalSynthetic' in field}
