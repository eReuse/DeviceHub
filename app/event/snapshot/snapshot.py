from app.device.device import Device
from app.device.exceptions import DeviceNotFound, NoDevicesToProcess
from app.exceptions import InnerRequestError
from app.rest import execute_post
from .event_processor import EventProcessor


class Snapshot:
    def __init__(self, device: dict, components: list):
        self.events = EventProcessor()
        self.device = device
        self.components = components
        self.unsecured = []

    def execute(self):
        event_log = []
        self.register(event_log)
        for component in self.components:
            self.get_add_remove(component, self.device)
        self._remove_nonexistent_components()
        return event_log + self.events.process()

    def get_add_remove(self, device: dict, new_parent: dict):
        """
        Get the changes (events) that will need to be triggered for the given device.
        Changes will we saved in the same device in the reserved key '_change'.
        The function doesn't execute any event per se or validate that the user can do it.

        :param device: The device must have an hid
        :param new_parent:
        """
        if 'new' not in device:
            try:
                old_parent = Device.get_parent(device['_id'])
            except DeviceNotFound:  # The component exists but had no parent device, until now
                self.events.append_add(device, new_parent)
            else:
                if not Device.seem_equal(old_parent, new_parent):
                    self.events.append_remove(device, old_parent)
                    self.events.append_add(device, new_parent)
        else:
            del device['new']

    def _remove_nonexistent_components(self):
        """
        This function needs to be executed at the end, after all components are in the DB and have _id

        In this stage, we have already added the components to the parent device. In the materialized components field
        of device we still have the old components. We need to remove those that are not present in this new snapshot.
        """
        if 'components' in self.device:
            for component_to_remove in Device.difference(self.device['components'], self.components):
                self.events.append_remove(component_to_remove, self.device)

    def _append_unsecured(self, device: dict, type: str):
        self.unsecured.append({'@type': device['@type'], 'type': type, '_id': device['_id']})

    def register(self, event_log: list):
        try:
            event_log.append(execute_post('register', {'@type': 'Register', 'device': self.device, 'components': self.components}))
        except NoDevicesToProcess:  # As it is a custom exception we throw, it keeps being an exception through post_internal
            pass
        for device in [self.device] + self.components:
            if 'hid' not in device and 'pid' not in device:
                self._append_unsecured(device, 'model')
            elif 'pid' in device:
                self._append_unsecured(device, 'pid')
