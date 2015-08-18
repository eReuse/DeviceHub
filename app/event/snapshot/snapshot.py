from cerberus import Validator

from app.device.Device import Device
from app.device import settings
from app.event.snapshot.EventProcessor import EventProcessor
from app.exceptions import ValidationError

__author__ = 'Xavier Bustamante Talavera'


class Snapshot:
    def __init__(self, device: dict, components: dict):
        self.validator = Validator(settings.device)
        self.events = EventProcessor()
        self.device = device
        self.components = components

    def prepare(self):
        self.validate(self.device)  # We validate against the schema
        Device.compute_hid(self.device)  # Then we try to generate the hid
        self.get_events(self.device)  # We get the events that will be need to be performed
        for component in self.components:
            self.validate(component)
            Device.compute_hid(component)
            self.get_events(component, self.device)
        self.events.check_viability()

    def validate(self, device: dict):
        if not self.validator.validate(device):
            raise ValidationError(self.validator.errors)

    def process(self) -> list:
        return self.events.process()

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
            old_parent = Device.get_parent(existing_device['_id'])
            if old_parent is not None:
                if new_parent is None or not Device.seem_equal(old_parent, new_parent):    # todo implement seem_equals
                    #  Parents differ, so we need to remove it from the old parent
                    self.events.add_remove(device, old_parent)
            if new_parent is not None:
                self.events.add_add(device, new_parent)
            if len(new_components) > 0:
                repeating_components = set(new_components).intersection(existing_device.components)
                orphaned_components = set(existing_device.components) - repeating_components
                # We apply it to the parent device as the orphaned components won't be processed by themselves
                for orphaned_component in orphaned_components:
                    self.events.add_remove(orphaned_component, device)

        else:
            self.events.add_insert(device)
            if new_parent is not None:
                # We don't apply 'register' to the parent device (parent device never will have another parent)
                self.events.add_register(device, new_parent)
