import copy
from contextlib import suppress
from pprint import pformat

from flask import current_app as app
from pydash import pluck
from rpy2.robjects import DataFrame, ListVector

from ereuse_devicehub.exceptions import StandardError
from ereuse_devicehub.export.export import SpreadsheetTranslator
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.device.component.domain import ComponentDomain
from ereuse_devicehub.resources.device.computer.settings import Computer
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.exceptions import DeviceNotFound, NoDevicesToProcess
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.rest import execute_post_internal
from ereuse_devicehub.utils import Naming
from .event_processor import EventProcessor


class SnapshotWithoutComponents:
    """
    Basic Snapshot that process devices without components; see *Snapshot* for more information.
    """

    def __init__(self, device: dict, components: list = None, created=None, parent: str = None):
        """

        :param device: The device to process.
        :param components: A list of components. Although not used in this class others do.
        :param created: Was the resource created?
        :param parent: The identifier of a parent, if the device is a component itself.
        """
        self.device = device
        self.components = components or []
        self.unsecured = []
        self.created = created
        self.parent = parent
        self.device_is_new = None
        self.new_components_id = {}

    def execute(self):
        event_log = []
        self.register(event_log)
        return event_log

    def register(self, event_log: list):
        with suppress(NoDevicesToProcess):
            register = {
                '@type': DeviceEventDomain.new_type('Register'),
                'device': self.device,
                'components': self.components,
                'parent': self.parent  # which can be None
            }
            self.set_created_conditionally(register)
            register = execute_post_internal(Naming.resource(register['@type']), register)
            self.device_is_new = register['deviceIsNew']
            self.new_components_id = set(register['components'])
            event_log.append(register)
        for device in [self.device] + self.components:
            if 'hid' not in device and 'pid' not in device:
                self._append_unsecured(device, 'model')
            elif 'pid' in device:
                self._append_unsecured(device, 'pid')

    def set_created_conditionally(self, resource):
        if self.created:
            resource['created'] = self.created

    def _append_unsecured(self, device: dict, resource_type: str):
        self.unsecured.append({'@type': device['@type'], 'type': resource_type, '_id': device['_id']})


class Snapshot(SnapshotWithoutComponents):
    """
    Updates devices and its components and performs events to the database to reflect
    the changes specified in Snapshot files, introduced as the init parameters.
    """

    def __init__(self, device: dict, components: list = None, created=None, parent: str = None):
        self.test_hard_drives = []
        self.erasures = []
        self.events = EventProcessor()
        super().__init__(device, components, created, parent)

    def execute(self):
        event_log = []
        self.get_tests_and_erasures(self.components)
        self.register(event_log)
        for component in self.components:
            self.get_add_remove(component, self.device)
        self.exec_hard_drive_events(event_log, self.erasures + self.test_hard_drives)
        self._remove_nonexistent_components()
        return event_log + self.events.process()

    def get_tests_and_erasures(self, components):
        for i, component in enumerate(components):
            if 'test' in component:
                self.test_hard_drives.append((i, component['test']))
                del component['test']
            if 'erasure' in component:
                self.erasures.append((i, component['erasure']))
                del component['erasure']

    def exec_hard_drive_events(self, event_log, events):
        for i, event in events:
            event['device'] = self.components[i]['_id']
            self.set_created_conditionally(event)
            event_log.append(execute_post_internal(Naming.resource(event['@type']), event))
            event.update(event_log[-1])

    def get_add_remove(self, device: dict, new_parent: dict):
        """
        Get the changes (events) that will need to be triggered for the given device.
        Changes will we saved in the same device in the reserved key '_change'.
        The function doesn't execute any event per se or validate that the user can do it.

        :param device: The device must have an hid
        :param new_parent:
        """
        if not device['_id'] in self.new_components_id:
            try:
                old_parent = ComponentDomain.get_parent(device['_id'])
            except DeviceNotFound:  # The component exists but had no parent device, until now
                self.events.append_add(device, new_parent)
            else:
                if not DeviceDomain.seem_equal(old_parent, new_parent):
                    self.events.append_remove(device, old_parent)
                    self.events.append_add(device, new_parent)

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
