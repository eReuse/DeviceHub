from bson import ObjectId
from eve.utils import document_etag
from flask import current_app
from flask import json

from ereuse_devicehub.exceptions import InnerRequestError
from ereuse_devicehub.resources.device.component.component import Component
from ereuse_devicehub.resources.device.exceptions import DeviceNotFound
from ereuse_devicehub.resources.event.event import Event
from ereuse_devicehub.rest import execute_get
from ereuse_devicehub.utils import Naming


class Device:
    """
    Class Device.

    Device get methods need to construct the element using the hooks, so they call internally using REST methods,
    not directly from the database.
    """

    # todo use get_internal when released for get_one and get_many methods

    @staticmethod
    def get_one(identifier_or_where: str or int or dict or ObjectId) -> dict:
        """
        Gets a single device.

        :param identifier_or_where: hid or _id
        :raises DeviceNotFound:
        :raises InnerRequestError: For any other type of error
        :return: Full Device
        """
        if type(identifier_or_where) is dict:
            try:
                device = Device.get_many(identifier_or_where)[0]
            except IndexError:
                raise DeviceNotFound()
        else:
            try:
                device = execute_get(
                    current_app.auth.get_requested_database_for_uri() + 'devices' + '/' + str(identifier_or_where))
            except InnerRequestError as e:
                if e.status_code == 404:
                    raise DeviceNotFound()
                else:
                    raise e
        return device

    @staticmethod
    def get_many(where):
        response = execute_get(
            current_app.auth.get_requested_database_for_uri() + 'devices' + '/' + '?where=' + json.dumps(where))
        return response['_items']

    @staticmethod
    def get_by_pid(pid: str) -> dict:
        """
        Gets a single device, using the pid.
        :param pid:
        :return:
        """
        try:
            database = current_app.auth.get_requested_database_for_uri()
            device = execute_get(database + 'devices?where={"pid":"' + pid + '"}')[0]
        except KeyError:
            raise DeviceNotFound()
        else:
            return device

    @staticmethod
    def get_parent(_id: str) -> dict or None:
        """

        :param _id:
        :raises DeviceNotFound:
        :return:
        """
        return Device.get_one({'components': {'$in': [_id]}})

    @staticmethod
    def get_similar_component(component: dict, parent_id: str) -> dict:
        # We the unsecured _id of the devices of all parent_id snapshots
        snapshots = Event.get({'@type': 'Snapshot', 'device': parent_id})
        devices_id = set()
        for snapshot in snapshots:
            for unsecured in snapshot['unsecured']:
                devices_id.add(unsecured['_id'])
        # We get the devices whose _id and etag matches
        etag = Device.generate_etag(component)
        query = {'_id': {'$in': list(devices_id)}, '_etag': etag}
        device = Device.get_one(query)
        if device is None:
            raise DeviceNotFound()
        else:
            return Device.get_one(device['_id'])  # todo if we materialize components we do not need to do double query

    @staticmethod
    def generate_etag(device: dict) -> str:
        return document_etag(device,
                             current_app.config['DOMAIN'][Naming.resource(device['@type'])]['etag_ignore_fields'])

    @staticmethod
    def seem_equal(x: dict, y: dict) -> bool:
        x_tag = x['_etag'] if '_etag' in x else Device.generate_etag(x)
        y_tag = y['_etag'] if '_etag' in y else Device.generate_etag(y)
        return x_tag == y_tag

    @staticmethod
    def difference(list_to_remove_devices_from, checking_list):
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
                if Device.seem_equal(x, y):
                    found = True
            if not found:
                difference.append(x)
        return difference

    @staticmethod
    def get_types():
        return Component.get_types_of_components() + Device.get_direct_subclasses()

    @staticmethod
    def get_direct_subclasses():
        return 'Peripheral', 'Monitor', 'Mobile', 'Computer', 'Component', 'DummyDevice'

    @staticmethod
    def resource_types():
        return (Naming.resource(event) for event in Device.get_types())

    @staticmethod
    def get_devices_with_components(devices_id: list) -> list:
        """
        Gets a list of devices with their components, not more values.
        :param devices_id:
        :return:
        """
        return Device.get_many({'_id': {'$in': devices_id}})

    @staticmethod
    def get_components_in_set(devices_id: list) -> set:
        """
        For a given list of devices, gets one set containing the union of all of their components
        :param devices_id:
        :return:
        """
        components = set()
        for device in Device.get_devices_with_components(list(devices_id)):
            if 'components' in device:
                components |= set(device['components'])
        return components

    @staticmethod
    def set_properties_internal(ids: str or list, properties: dict):
        Device.update(ids, {'$set': properties})

    @staticmethod
    def update(ids: str or list, operation: dict):
        """
        Sets the properties of a device using directly the database layer. The method just updates the keys in
        properties. Properties can use mongodb parameters.
        """
        devices_id = [ids] if type(ids) is str else ids
        for device_id in devices_id:
            current_app.data.driver.db['devices'].update_one({'_id': device_id}, operation)

    @staticmethod
    def benchmark(component: dict):
        """
        Adds the result of a benchmark to a component.

        Components needs to exist in the database.
        :param component:
        """
        assert '_id' in component, 'Component needs to be created'
        if 'benchmark' in component:
            Device.update(component['_id'], {'$push': {'benchmarks': component['benchmark']}})
