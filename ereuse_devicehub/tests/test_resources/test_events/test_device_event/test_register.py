import copy

from assertpy import assert_that

from ereuse_devicehub.tests.test_resources.test_events import TestEvent


class TestRegister(TestEvent):
    REGISTER = 'register'

    def test_register_placeholder(self):
        """Tests registering a placeholder, moving it to a place and discovering it."""
        placeholder = self.get_fixture('register', '1-placeholder')
        event = self.post_and_check('{}/{}'.format(self.DEVICE_EVENT, self.REGISTER), placeholder)
        device, status = self.get(self.DEVICES, '', event['device'])
        self.assert200(status)
        assert_that(device['@type']).is_equal_to('Device')
        assert_that(device['placeholder']).is_true()
        # Let's add the device to a place
        place = self.get_fixture(self.PLACES, 'place')
        place['devices'] = [device['_id']]
        place = self.post_and_check(self.PLACES, copy.deepcopy(place))
        self.device_and_place_contain_each_other(device['_id'], place['_id'])
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
        self.device_and_place_contain_each_other(updated_device['_id'], place['_id'])
