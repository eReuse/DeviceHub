from app.device.Device import Device
from .EventProcessor import EventProcessor


__author__ = 'Xavier Bustamante Talavera'


class Snapshot:
    def __init__(self, device: dict, components: dict):
        self.events = EventProcessor()
        self.device = device
        self.components = components

    def prepare(self):
        """
        We don't need to validate devices against the schema as it's has already been done in snapshot's schema
        :return:
        """
        Device.compute_hid(self.device)  # Then we try to generate the hid
        self.get_events(self.device)  # We get the events that will be need to be performed
        for component in self.components:
            Device.compute_hid(component)
            self.get_events(component, self.device)
        self.events.check_viability()

    def process(self) -> list:
        executed_events = self.events.process()
        return executed_events

    def get_events(self, device: dict, new_parent: dict=None, new_components: list=list()):
        """
        Get the changes (events) that will need to be triggered for the given device.
        Changes will we saved in the same device in the reserved key '_change'.
        The function doesn't execute any event per se or validate that the user can do it.
        :param device:
        :param new_parent:
        """
        existing_device = Device.get_device_by_identifiers(device)
        if existing_device is not None:
            device['_id'] = existing_device['_id']
            old_parent = Device.get_parent(existing_device['_id'])
            if old_parent is not None:
                if new_parent is None or not Device.seem_equal(old_parent, new_parent):
                    #  Parents differ, so we need to remove it from the old parent
                    self.events.add_remove(existing_device, old_parent)
            if new_parent is not None:
                self.events.add_add(existing_device, new_parent)
            if len(new_components) > 0:
                repeating_components = set(new_components).intersection(existing_device['components'])
                orphaned_components = set(existing_device['components']) - repeating_components
                # We apply it to the parent device as the orphaned components won't be processed by themselves
                for orphaned_component in orphaned_components:
                    self.events.add_remove(orphaned_component, existing_device)

        else:
            self.events.add_insert(device)
            if new_parent is not None:
                # We don't apply 'register' to the parent device (parent device never will have another parent)
                self.events.add_register(device, new_parent)
