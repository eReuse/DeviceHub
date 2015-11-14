from bson import ObjectId

from app.device.device import Device
from .event_processor import EventProcessor
from app.exceptions import InnerRequestError


class Snapshot:
    def __init__(self, device: dict, components: list):
        self.events = EventProcessor()
        self.device = device
        self.components = components

    def prepare(self):
        """
        We don't need to validate devices against the schema as it's has already been done in snapshot's schema
        :return:
        """
        Device.compute_hid(self.device)  # Then we try to generate the hid
        self.get_events(self.device, None, self.components)  # We get the events that will be need to be performed
        for component in self.components:
            Device.compute_hid(component)
            self.get_events(component, self.device)
        self.remove_nonexistent_components(self.device, self.components)
        self.events.check_viability()

    def process(self) -> list:
        executed_events = self.events.process()
        return executed_events

    def get_events(self, device: dict, new_parent: dict = None, new_components: list = list()):
        """
        Get the changes (events) that will need to be triggered for the given device.
        Changes will we saved in the same device in the reserved key '_change'.
        The function doesn't execute any event per se or validate that the user can do it.

        :param device:
        :param new_parent:
        """
        try:
            existing_device = Device.get_device_by_identifiers(device)
        except InnerRequestError as ie:
            if ie.status_code != 404:
                raise ie
            else:
                self.events.add_insert(device)
                if new_parent is not None:
                    # We don't apply 'register' to the parent device (parent device never will have another parent)
                    self.events.add_register(device, new_parent)
        else:
            device['_id'] = existing_device['_id']
            if 'components' in existing_device:  # todo can exist empty lists of components?
                device['components'] = existing_device[
                    'components']  # todo make sure components are or full object or objectid
            old_parent = Device.get_parent(ObjectId(existing_device['_id']))
            if old_parent is not None:
                if new_parent is None or not Device.seem_equal(old_parent, new_parent):
                    #  Parents differ, so we need to remove it from the old parent
                    self.events.add_remove(existing_device, old_parent)
            if new_parent is not None:
                if old_parent is not None and not Device.seem_equal(old_parent, new_parent):  # todo sure?
                    self.events.add_add(existing_device, new_parent)

    def remove_nonexistent_components(self, device, new_components):
        """
        This function needs to be executed at the end, after all new components have been inserted (and hid generated...)
        :param device:
        :param new_components:
        :return:
        """
        if 'components' in device:
            for component_to_remove in Device.difference(device['components'], new_components):
                self.events.add_remove(component_to_remove, device)
