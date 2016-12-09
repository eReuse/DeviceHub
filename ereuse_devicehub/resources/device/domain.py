from ereuse_devicehub.resources.device.exceptions import DeviceNotFound
from ereuse_devicehub.resources.device.settings import DeviceSettings
from ereuse_devicehub.resources.domain import Domain, ResourceNotFound
from ereuse_devicehub.utils import Naming
from eve.utils import document_etag
from flask import current_app


class DeviceDomain(Domain):
    resource_settings = DeviceSettings

    @classmethod
    def get_one(cls, id_or_filter: str or dict) -> dict:
        """
        :throws DeviceNotFound:
        """
        try:
            return super().get_one(id_or_filter)
        except ResourceNotFound:
            raise DeviceNotFound()

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
            found = False
            for y in checking_list:
                if cls.seem_equal(x, y):
                    found = True
            if not found:
                difference.append(x)
        return difference
