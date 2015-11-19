from bson import ObjectId
from eve.methods.delete import deleteitem_internal
from app.app import app

from app.device.device import Device, DeviceNotFound
from app.device.exceptions import HidError
from app.utils import get_resource_name
from .event_processor import EventProcessor
from app.exceptions import InnerRequestError


class Snapshot:
    def __init__(self, device: dict, components: list):
        self.events = EventProcessor()
        self.device = device
        self.components = components
        self.warnings = []
        self.unsecured = []

    def prepare(self):
        """
        We don't need to validate devices against the schema as it's has already been done in snapshot's schema
        :return:
        """
        try:
            try:
                Device.normalize_and_compute_hid(self.device)  # Then we try to generate the hid
                self._get_device_by_hid_and_update_device(self.device)
            except HidError:
                self._get_device_by_pid_and_update_device(self.device['pid'])  # if not found will throw error
                self._add_warning(self.device, 'CannotGenerateHIDUsedPid')
        except (DeviceNotFound, KeyError):
            self.events.add_register_parent(self.device)
        for component in self.components:
            try:
                try:
                    Device.normalize_and_compute_hid(component)
                    self._get_device_by_hid_and_update_device(component)
                except HidError:
                    self.unsecured.append(component)
                    try:
                        self._get_device_by_pid_and_update_device(component['pid'])
                        self._add_warning(component, 'CannotGenerateHIDUsedPid')
                    except (DeviceNotFound, KeyError):
                        component['_id'] = self._get_similar_component_id(component)
            except DeviceNotFound:
                self.events.add_register_component(component)
            else:
                self.get_add_remove(component, self.device)
        self._remove_nonexistent_components()

    # noinspection PyBroadException
    def process(self) -> list:
            return self.events.process()

    @staticmethod
    def _get_device_by_hid_and_update_device(device: dict):
        existing_device = Device.get_device_by_hid(device['hid'])
        device['_id'] = existing_device['_id']
        device['components'] = existing_device['components']

    @staticmethod
    def _get_device_by_pid_and_update_device(device: dict):
        existing_device = Device.get_device_by_pid(device['pid'])
        device['_id'] = existing_device['_id']
        device['components'] = existing_device['components']

    def get_add_remove(self, device: dict, new_parent: dict):
        """
        Get the changes (events) that will need to be triggered for the given device.
        Changes will we saved in the same device in the reserved key '_change'.
        The function doesn't execute any event per se or validate that the user can do it.

        :param device: The device must have an hid
        :param new_parent:
        """
        try:
            old_parent = Device.get_parent(device['_id'])
        except DeviceNotFound:  # The component exists but had no parent device, until now
            self.events.add_add(device, new_parent)
        else:
            if not Device.seem_equal(old_parent, new_parent):
                self.events.add_remove(device, old_parent)
                self.events.add_add(device, new_parent)

    def _remove_nonexistent_components(self):
        """
        This function needs to be executed at the end, after all components are in the DB and have _id

        In this stage, we have already added the components to the parent device. In the materialized components field
        of device we still have the old components. We need to remove those that are not present in this new snapshot.
        """
        for component_to_remove in Device.difference(self.device['components'], self.components):
            self.events.add_remove(component_to_remove, self.device)

    def _add_warning(self, device: dict, type: str):
        self.warnings.append({'@type': device['@type'], 'type': type})

    def _get_similar_component_id(self, component: dict) -> dict:
        try:
            snapshots = list(app.data.driver.db['events'].find({'@type': 'Snapshot', 'device': self.device['_id']}))
            unsecured = []
            for snapshot in snapshots:
                unsecured += snapshot['unsecured']
            query = {'_id': {'$in': unsecured}, '@type': component['@type'],
                     'model': component['model']}
        except KeyError:  # if _id or
            raise DeviceNotFound('ParentNo_idOrComponentNoModel')
        else:
            device = app.data.driver.db['devices'].find_one(query)
            if device is None:
                raise DeviceNotFound()
            else:
                return device['_id']

    def delete_events(self, events: list):
        """
        Deletes the events and inserts (the latter deleting the device). The deletion is done in reverse order.


        """

        # for event in events:
        #    deleteitem_internal(get_resource_name(event['@type']), event)
