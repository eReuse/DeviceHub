from flask import g

from ereuse_devicehub.resources.device.component.domain import ComponentDomain
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.exceptions import DeviceNotFound, NoDevicesToProcess
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.rest import execute_post
from ereuse_devicehub.utils import Naming
from .event_processor import EventProcessor


class Snapshot:
    def __init__(self, device: dict, components: list):
        self.events = EventProcessor()
        self.device = device
        self.components = components
        self.unsecured = []
        self.test_hard_drives = g.snapshot_test_hard_drives = []
        self.erasures = g.snapshot_basic_erasures = []

    def execute(self):
        event_log = []
        self.get_tests_and_erasures(self.components)
        self.register(event_log)
        for component in self.components:
            self.get_add_remove(component, self.device)
        self.exec_hard_drive_events(event_log, self.erasures + self.test_hard_drives)
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
                old_parent = ComponentDomain.get_parent(device['_id'])
            except DeviceNotFound:  # The component exists but had no parent device, until now
                self.events.append_add(device, new_parent)
            else:
                if not DeviceDomain.seem_equal(old_parent, new_parent):
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
            full_old_components = [ComponentDomain.get_one(component) for component in self.device['components']]
            for component_to_remove in ComponentDomain.difference(full_old_components, self.components):
                self.events.append_remove(component_to_remove, self.device)

    def _append_unsecured(self, device: dict, resource_type: str):
        self.unsecured.append({'@type': device['@type'], 'type': resource_type, '_id': device['_id']})

    def register(self, event_log: list):
        try:
            register = {
                '@type': DeviceEventDomain.new_type('Register'),
                'device': self.device,
                'components': self.components
            }
            event_log.append(execute_post(Naming.resource(register['@type']), register))
        except NoDevicesToProcess:  # As it is a custom exception we throw, it keeps being an exception through post_internal
            pass
        for device in [self.device] + self.components:
            if 'hid' not in device and 'pid' not in device:
                self._append_unsecured(device, 'model')
            elif 'pid' in device:
                self._append_unsecured(device, 'pid')

    def get_tests_and_erasures(self, components):
        i = 0
        for component in components:
            if 'test' in component:
                self.test_hard_drives.append((i, component['test']))
                del component['test']
            if 'erasure' in component:
                self.erasures.append((i, component['erasure']))
                del component['erasure']
            i += 1

    def exec_hard_drive_events(self, event_log, events):
        for i, event in events:
            event['device'] = self.components[i]['_id']
            event_log.append(execute_post(Naming.resource(event['@type']), event))
            event.update(event_log[-1])
