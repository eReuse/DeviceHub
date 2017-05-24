from assertpy import assert_that

from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent
from ereuse_devicehub.tests.test_resources.test_group import TestGroupBase


class TestLocate(TestDeviceEvent, TestGroupBase):
    LOCATE = 'locate'
    POST_LOCATE = TestDeviceEvent.DEVICE_EVENT + '/locate'

    def test_create_locate_with_place(self):
        locate = self.get_fixture(self.LOCATE, 'locate')
        locate['place'] = self.place['_id']
        locate['devices'] = self.devices_id
        locate = self.post_and_check(self.POST_LOCATE, locate)
        # Let's check the place has been correctly materialized in the devices
        for device_id in self.devices_id:
            self.is_parent(self.place['_id'], self.PLACES, device_id, self.DEVICES)
        return locate

    def test_delete(self):
        locate = self.test_create_locate_with_place()
        self.delete_and_check(self.POST_LOCATE + '/' + locate['_id'])
        _, status = self.get(self.LOCATE, '', locate['_id'])
        self.assert404(status)
        # let's check the place has been de-materialized in the devices
        for device_id in self.devices_id:
            self.devices_do_not_contain_places(device_id)
        # Let's check locate has been de-materialized in the devices
        for device_id in self.devices_id:
            device, _ = self.get(self.DEVICES, '', device_id)
            assert_that(device['events']).extracting('_id').does_not_contain(locate['_id'])

    def test_create_locate_with_coordinates(self):
        # Let's create a location with coordinates without a place that contains them. It will give us error.
        locate = self.get_fixture(self.LOCATE, 'locate_with_coordinates')
        locate['devices'] = self.devices_id
        _, status = self.post(self.POST_LOCATE, locate)
        self.assert400(status)
        # Now we create the place
        place = self.post_fixture(self.PLACES, self.PLACES, 'place_with_coordinates')
        # We repeat the location. As the coordinates are in the area of the place, we can create it
        locate = self.post_and_check(self.POST_LOCATE, locate)
        # Let's check if locate has been assigned to the place
        locate, _ = self.get(self.DEVICE_EVENT, '', locate['_id'])
        self.assertIn('place', locate)
        self.assertEqual(locate['place'], place['_id'])
        # Let's assure that the materializations of the devices are correct
        for device_id in self.devices_id:
            device, _ = self.get(self.DEVICES, item=device_id)
            place, _ = self.get(self.PLACES, item=place['_id'])
            self.is_parent(place['_id'], self.PLACES, device_id, self.DEVICES)
            assert_that(device['events'][0]).is_subset_of(locate)

    def test_monitor(self):
        """
        The same as test_create_locate_with_coordiantes but with a monitor
        """
        locate = self.get_fixture(self.LOCATE, 'locate_with_coordinates')
        snapshot = self.post_fixture(self.SNAPSHOT, '{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), 'monitor')
        snapshot, _ = self.get('devices_snapshot', '', snapshot['_id'])
        locate['devices'] = [self.get(self.DEVICES, '', snapshot['device'])[0]['_id']]
        # Let's directly create a place
        place = self.post_fixture(self.PLACES, self.PLACES, 'place_with_coordinates')
        # We repeat the location. As the coordinates are in the area of the place, we can create it
        locate = self.post_and_check(self.POST_LOCATE, locate)
        # Let's check if locate has been assigned to the place
        locate, _ = self.get(self.DEVICE_EVENT, '', locate['_id'])
        self.assertIn('place', locate)
        self.assertEqual(locate['place'], place['_id'])
        # Let's assure that the materializations of computerMonitor are correct
        computer_monitor, _ = self.get(self.DEVICES, '', snapshot['device'])
        place, _ = self.get(self.PLACES, item=place['_id'])
        self.is_parent(place['_id'], self.PLACES, computer_monitor['_id'], self.DEVICES)
        assert_that(computer_monitor['events'][0]).is_subset_of(locate)
