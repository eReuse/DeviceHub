from datetime import timedelta
from time import sleep

from assertpy import assert_that
from bson import ObjectId
from pydash import pick

from ereuse_devicehub.exceptions import SchemaError
from ereuse_devicehub.resources.hooks import TooLateToDelete, MaterializeEvents
from ereuse_devicehub.tests import TestStandard
from ereuse_devicehub.utils import Naming


class TestDeviceEventBasic(TestStandard):
    """
        Tests that take care of the creation and configuration of device events.
    """

    def test_creation(self):
        """
        Tests that device events have been created correctly, taking special care of:
        - All events have been created
        - @type and type
        - URL
        - prefix
        """
        events = ('add', 'allocate', 'deallocate', 'dispose', 'free',
                  'locate', 'ready', 'receive', 'register', 'remove', 'repair', 'snapshot', 'test-hard-drive',
                  'to-dispose', 'to-repair', 'to-prepare')  # all subclasses from DeviceEvent in resource type
        events = ['{}{}{}'.format('devices', Naming.RESOURCE_PREFIX, event) for event in events]  # we prefix them
        events += ['accounts', 'devices', 'computer']  # We check some non-prefixed regular resources...
        assert_that(self.domain).contains_key(*events)
        # Type of snapshot should be 'devices:Snapshot'
        snapshot = self.domain['{}{}{}'.format('devices', Naming.RESOURCE_PREFIX, 'snapshot')]
        assert_that(snapshot['schema']['@type']['allowed']) \
            .is_equal_to({'{}{}{}'.format('devices', Naming.TYPE_PREFIX, 'Snapshot')})
        devices = self.domain['devices']
        # And any other type not subclass from DeviceEvent should be without prefix
        assert_that(devices['schema']['@type']['allowed']).contains('Device', 'Computer', 'HardDrive')  # ...and more

        # Checking that the url generated contains 'devices' for DeviceEvent...
        assert_that(snapshot['url']).is_equal_to('events/devices/snapshot')
        # ...but it doesn't add devices to others (it would be then 'devices/devices')
        assert_that(devices['url']).is_equal_to('devices')

    def test_delete_in_time(self):
        """Tests deleting an event only in time."""
        # Let's set a small amount of time and try to delete the device after it
        self.app.config['TIME_TO_DELETE_RESOURCES'] = timedelta(seconds=1)
        SNAPSHOT_URL = self.DEVICE_EVENT + '/' + self.SNAPSHOT
        snapshot = self.post_fixture(self.SNAPSHOT, SNAPSHOT_URL, 'xps13')
        sleep(2)
        response, status = self.delete(SNAPSHOT_URL, item=snapshot['_id'])
        self.assert_error(response, status, TooLateToDelete)

    def test_groups(self):
        """Tests a generic event with the 'groups' field set."""
        # Let's create a lot and a package, both with 2 different devices
        computers_id = self.get_fixtures_computers()
        lot = self.get_fixture(self.GROUPS, 'lot')
        lot['children']['devices'] = computers_id[0:2]
        lot = self.post_and_check(self.LOTS, lot)
        package = self.get_fixture(self.GROUPS, 'package')
        package['children']['devices'] = computers_id[2:4]
        package = self.post_and_check(self.PACKAGES, package)
        # Let's post the event
        READY_URL = '{}/{}'.format(self.DEVICE_EVENT, 'ready')
        ready = self.get_fixture(self.GROUPS, 'ready')
        ready['groups']['lots'] = [lot['_id']]
        ready['groups']['packages'] = [package['_id']]
        ready = self.post_and_check(READY_URL, ready)

        self._check(lot['_id'], package['_id'], computers_id, ready['_id'])

        # If we try to do an event with both devices and a groups
        ready = self.get_fixture(self.GROUPS, 'ready')
        ready['devices'] = computers_id
        response, status = self.post(READY_URL, ready)
        self.assert_error(response, status, SchemaError)

        # Now let's try with descendants
        # We add one new extra device to package
        snapshot = self.post_fixture(self.SNAPSHOT, '{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), 'vaio')
        package['children']['devices'].append(snapshot['device'])
        self.patch_and_check(self.PACKAGES, item=package['_id'], payload=pick(package, 'children', '@type'))
        # adding package inside lot and event with only lot. The event should be done to package and its devices
        lot['children']['packages'] = [package['_id']]
        self.patch_and_check(self.LOTS, item=lot['_id'], payload=pick(lot, 'children', '@type'))
        receive = self.get_fixture('receive', 'receive')
        receive['groups'] = {'lots': [lot['_id']]}
        receive['receiver'] = self.get_first('accounts')['_id']
        receive = self.post_and_check('{}/{}'.format(self.DEVICE_EVENT, 'receive'), receive)

        # Preparing to check
        self._check(lot['_id'], package['_id'], computers_id + [snapshot['device']], receive['_id'])

        # Try if label does not exist
        package['children']['devices'].append('This label does not exist')
        _, status = self.patch(self.PACKAGES, item=package['_id'], data=pick(package, 'children', '@type'))
        self.assert422(status)

    def _check(self, lot_id: str, package_id: str, computers_id: list, event_id: ObjectId):
        """Checks that the event contains the devices and groups, and otherwise."""
        event = self.get_and_check(self.EVENTS, item=event_id)
        materialized_event = pick(event, *MaterializeEvents.FIELDS)
        lot = self.get_and_check(self.LOTS, item=lot_id)
        package = self.get_and_check(self.PACKAGES, item=package_id)
        # Both event and groups contain each other
        assert_that(event['groups']).has_lots([lot_id]).has_packages([package_id])
        lot = self.get_and_check(self.LOTS, item=lot['_id'])
        assert_that(lot['events']).contains(materialized_event)
        package = self.get_and_check(self.PACKAGES, item=package['_id'])
        assert_that(package['events']).contains(materialized_event)
        # Both event and devices contain each other
        assert_that(event).contains('devices')
        assert_that(event['devices']).contains_only(*computers_id)
        for computer_id in computers_id:
            computer = self.get_and_check(self.DEVICES, item=computer_id, embedded={'components': True})
            assert_that(computer['events']).contains(materialized_event)
            # Let's ensure the events have been materialized for components too
            for component in computer['components']:
                assert_that(component['events']).contains(materialized_event)
