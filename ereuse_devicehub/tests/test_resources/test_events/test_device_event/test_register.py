import copy

from assertpy import assert_that
from pydash import pick

from ereuse_devicehub.resources.hooks import MaterializeEvents
from ereuse_devicehub.tests.test_resources.test_events import TestEvent
from ereuse_devicehub.tests.test_resources.test_group import TestGroupBase


class TestRegister(TestEvent, TestGroupBase):
    REGISTER = 'register'
    REGISTER_URL = '{}/{}'.format(TestEvent.DEVICE_EVENT, REGISTER)

    def test_register_placeholder(self):
        """Tests registering a placeholder, moving it to a place and discovering it."""
        placeholder = self.get_fixture('register', '1-placeholder')
        event = self.post_and_check(self.REGISTER_URL, placeholder)
        event = self.get_and_check(self.EVENTS, item=event['_id'])
        device = self.get_and_check(self.DEVICES, '', event['device'])
        assert_that(device['@type']).is_equal_to('Device')
        assert_that(device['placeholder']).is_true()
        assert_that(device).has_events([pick(event, *MaterializeEvents.FIELDS)])  # Materialization on device is ok
        # Let's add the device to a place
        place = self.get_fixture(self.PLACES, 'place')
        place['children'] = {'devices': [device['_id']]}
        place = self.post_and_check(self.PLACES, copy.deepcopy(place))
        self.is_parent(place['_id'], self.PLACES, device['_id'], self.DEVICES)
        # Let's discover the device
        full_snapshot = self.get_fixture('register', '1-full-snapshot')
        # The device of the snapshot links to the placeholder through the id
        # This is the only difference with a regular Snapshot (regular snapshots do not *usually* have an '_id')
        full_snapshot['device']['_id'] = device['_id']
        full_snapshot = self.post_and_check('{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), full_snapshot)
        assert_that(full_snapshot['device']).is_equal_to(device['_id'])
        updated_device, _ = self.get(self.DEVICES, '', event['device'])
        assert_that(updated_device['placeholder']).is_false()
        # The @type of device has changed as the part of the discovery
        assert_that(updated_device['@type']).is_equal_to('Computer')
        # The device and its components need to be in the same place as before
        self.is_parent(place['_id'], self.PLACES, updated_device['_id'], self.DEVICES)

    def test_placeholder_endpoint(self):
        """Tests the placeholder endpoint."""
        response = self.post_and_check('events/devices_register/placeholders?quantity=3', {})
        assert_that(response).is_equal_to({'devices': ['1', '2', '3']})
        for device_id in response['devices']:
            device = self.get_and_check(self.DEVICES, item=device_id)
            assert_that(device['@type']).is_equal_to('Device')
            assert_that(device).has_placeholder(True)
