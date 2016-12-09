from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.exceptions import DeviceNotFound
from ereuse_devicehub.resources.event.device.snapshot.snapshot import Snapshot


class MigrateCreator(Snapshot):
    def __init__(self, device: dict, components: list, created=None):
        self.urls = []
        self.returned_same_as = dict()  # Field in migrate
        super().__init__(device, components, created)

    def execute(self):
        """Like Snapshot's one, but removing everything related with tests and erasures"""
        event_log = []
        same_as_found_components = []
        same_as_found = self.process_same_as(self.device)
        for component in self.components:
            same_as_found_components.append(self.process_same_as(component))
        self.register(event_log)
        self.warn_for_broken_same_as(same_as_found, same_as_found_components)
        self.update_same_as(same_as_found, same_as_found_components)
        for component in self.components:
            self.get_add_remove(component, self.device)
        self._remove_nonexistent_components()
        self.generate_returned_same_as()
        return event_log + self.events.process()

    def get_tests_and_erasures(self, components):
        raise NotImplementedError()

    def exec_hard_drive_events(self, event_log, events):
        raise NotImplementedError()

    def process_same_as(self, device: dict) -> (bool, list):
        """
        Tries to match the input device with an existing one by detecting a similar url in sameAs and url fields, and
        then processes them.

        Given a set of sameAs and url in the param device, it tries to find at least one of those url ones in another
        device in the database. If found, both devices are thought to be the same and both 'sameAs' fields are merged
        (note that Register does update the sameAs).

        :param device: The device to check if whose sameAs and URL match any of the already existing ones.
        :return: A boolean indicating if a device was found in the database with at least one matching url and a list
        of sameAs for the device
        """
        urls = [device['url']] + device.get('sameAs', [])
        self.urls.append(device.pop('url'))
        matching_same_as = False
        try:
            already_existing_device = DeviceDomain.get_one({'sameAs': {'$in': urls}})
        except DeviceNotFound:
            same_as = device['sameAs'] = urls
        else:
            device['_id'] = already_existing_device['_id']
            urls_set = set(urls)
            # we do not want the url of the existing device to be part of the sameAs
            urls_set.discard(already_existing_device.get('url'))
            same_as = device['sameAs'] = list(set(already_existing_device['sameAs']) | urls_set)
            matching_same_as = True
        return matching_same_as, same_as

    def warn_for_broken_same_as(self, same_as_found: (bool, list), same_as_found_components: list):
        """
        Adds those devices that had no sameAs but there were existing to the 'unsecured' field of the migrate.

        If the same device is registered twice in different databases and there is no GRD to detect the collision, it
        will only get in conflict when migrating one *twin* device to the other's database:
        `MigrateCreator.process_same_as` would have returned false for that device,
        however the device would not have been created. This situation is known as a **broken sameAs**
        (a reference that should have been existed in the sameAs), and it is noted as an unsecured device (like in
        Snapshot).

        :param same_as_found: a boolean stating if `self.device` had a matching sameAs (sameAs was found in the DB)
            and a list of sameAs
        :param same_as_found_components: list of booleans,
            each bool of the list represents a component (ordered equally)
        """
        if not same_as_found[0] and self.device['new']:
            self._append_unsecured(self.device, 'sameAs')
        for component, same_as_found_component in zip(self.components, same_as_found_components):
            if not same_as_found_component[0] and component['new']:
                self._append_unsecured(component, 'sameAs')

    def update_same_as(self, same_as_found, same_as_found_components):
        """
        Saves in the database the new value of sameAs.

        This only makes sense when the device has not been created (as it existed); Register does not update its values.
        """
        if not self.device['new']:
            self._update_same_as(self.device, same_as_found[1])
        for component, same_as_found_component in zip(self.components, same_as_found_components):
            if not component['new']:
                self._update_same_as(component, same_as_found_component[1])

    @staticmethod
    def _update_same_as(device: dict, same_as: list):
        DeviceDomain.update_one_raw(device['_id'], {'$set': {'sameAs': same_as}})

    def generate_returned_same_as(self):
        """
        Populates self.returned_same_as with a dict where the URL of devices in the caller agent as keys and a copy of
        'sameAs' in this agent.

        This value will be returned to the caller agent (see
        :py:func:`ereuse_devicehub.resources.event.device.migrate.hooks.return_same_as`) which can use it to update
        its 'sameAs' values with new references.
        """
        for device, url in zip([self.device] + self.components, self.urls):
            device = DeviceDomain.get_one(device['_id'])
            same_as = set(device['sameAs'])
            same_as.remove(url)
            same_as.add(DeviceDomain.url_agent_for(AccountDomain.get_requested_database(), device['_id']))
            self.returned_same_as[url] = list(same_as)
