from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.exceptions import DeviceNotFound
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.domain import EventDomain


class ComponentDomain(DeviceDomain):
    @classmethod
    def get_parent(cls, _id: str) -> dict or None:
        return cls.get_one({'components': {'$in': [_id]}})

    @classmethod
    def get_similar_component(cls, component: dict, parent_id: str) -> dict:
        """Gets a component that has same parent, doesn't generate HID and their ETAG are the same"""
        # We the unsecured _id of the devices of all parent_id snapshots
        snapshots = EventDomain.get({'@type': DeviceEventDomain.new_type('Snapshot'), 'device': parent_id})
        devices_id = set()
        for snapshot in snapshots:
            for unsecured in snapshot['unsecured']:
                devices_id.add(unsecured['_id'])
        # We get the devices whose _id and etag matches
        etag = cls.generate_etag(component)
        query = {'_id': {'$in': list(devices_id)}, '_etag': etag}
        device = cls.get_one(query)
        return cls.get_one(device['_id'])  # todo if we materialize components we do not need to do double query

    @classmethod
    def get_devices_with_components(cls, devices_id: list) -> list:
        """
        Gets a list of devices with their components, not more values.
        :param devices_id:
        :return:
        """
        return cls.get({'_id': {'$in': devices_id}})

    @classmethod
    def get_components_in_set(cls, devices_id: list) -> set:
        """
        For a given list of devices, gets one set containing the union of all of their components
        :param devices_id:
        :return:
        """
        components = set()
        for device in cls.get_devices_with_components(list(devices_id)):
            if 'components' in device:
                components |= set(device['components'])
        return components

    @classmethod
    def benchmark(cls, component: dict):
        """
        Adds the result of a benchmark to a component.

        Components needs to exist in the database.
        :param component:
        """
        assert '_id' in component, 'Component needs to be created'
        if 'benchmark' in component:
            cls.update_raw(component['_id'], {'$push': {'benchmarks': component['benchmark']}})
