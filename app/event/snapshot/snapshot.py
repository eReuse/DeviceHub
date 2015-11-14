from bson import ObjectId
from app.app import app

from app.device.device import Device, DeviceNotFound
from app.device.exceptions import HidError
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
            Device.compute_hid(self.device)  # Then we try to generate the hid
        except HidError as e:
            if 'pid' in self.device:
                self._add_warning(self.device, 'CannotGenerateHIDUsedPid')
            else:
                raise e
        self.get_events(self.device, None)  # We get the events that will be need to be performed
        for component in self.components:
            try:
                Device.compute_hid(component)
            except HidError:
                if 'pid' in self.device:
                    self._add_warning(self.device, 'CannotGenerateHIDUsedPid')
                else:
                    try:
                        component = self._get_similar_component(component)
                    except DeviceNotFound:
                        self._add_warning(self.device, 'NotFoundSimilarDevice')
                    else:
                        self.unsecured.append(component)
            else:
                self.get_events(component, self.device)
        self._remove_nonexistent_components()
        self.events.check_viability()

    def process(self) -> list:
        executed_events = self.events.process()
        return executed_events

    def get_events(self, device: dict, new_parent: dict = None):
        """
        Get the changes (events) that will need to be triggered for the given device.
        Changes will we saved in the same device in the reserved key '_change'.
        The function doesn't execute any event per se or validate that the user can do it.

        :param device: The device must have an hid
        :param new_parent:
        """
        try:
            existing_device = Device.get_device_by_hid(device)
        except DeviceNotFound:
            self.events.add_insert(device)
            if new_parent is not None:  # todo: register parent with no children
                # We register all the children with the parent at the same time
                self.events.add_register(device, new_parent)
        else:
            device['_id'] = existing_device['_id']
            device['components'] = existing_device['components']
            if new_parent is not None:
                try:
                    old_parent = Device.get_parent(ObjectId(existing_device['_id']))
                except DeviceNotFound:
                    pass  # The device is new :-)
                else:
                    if not Device.seem_equal_by_identifiers(old_parent, new_parent):
                        self.events.add_remove(existing_device, old_parent)
                        self.events.add_add(existing_device, new_parent)

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

    def _get_similar_component(self, component: dict) -> dict:
        if '_id' not in self.device:
            raise DeviceNotFound()
        snapshots = app.data.driver.db['events'].find({'@type': 'Snapshot', 'device': self.device['_id']})
        query = {'_id': {'$in': [snapshot['unsecured'] for snapshot in snapshots]}, '@type': component['@type'],
                 'model': component['model']}
        device = app.data.driver.db['devices'].find_one(query)
        if device is None:
            raise DeviceNotFound()
        else:
            return device




