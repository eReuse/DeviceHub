from assertpy import assert_that
from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent


class TestLocate(TestDeviceEvent):
    LOCATE = 'locate'
    POST_LOCATE = TestDeviceEvent.DEVICE_EVENT + '/locate'

    def test_create_locate_with_place(self):
        locate = self.get_fixture(self.LOCATE, 'locate')
        locate['place'] = self.place['_id']
        locate['devices'] = self.devices_id
        self.post_and_check(self.POST_LOCATE, locate)
        # Let's check the place has been correctly materialized in the devices
        for device_id in self.devices_id:
            self.device_and_place_contain_each_other(device_id, self.place['_id'])

    def test_create_locate_with_coordinates(self):
        # Let's create a location with coordinates without a place that contains them. It will give us error.
        locate = self.get_fixture(self.LOCATE, 'locate_with_coordinates')
        locate['devices'] = self.devices_id
        try:
            self.post_and_check(self.POST_LOCATE, locate)
        except AssertionError as e:
            if e.args[0] == '400 != 201':
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
                    device, _ = self.get(self.DEVICES, '', device_id)
                    self.assertEqual(place['_id'], device['place'])
                    assert_that(device['events'][0]).is_subset_of(locate)
            else:
                self.assertTrue(False)
        else:
            self.assertTrue(False)

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
        computerMonitor, _ = self.get(self.DEVICES, '', snapshot['device'])
        self.assertEqual(place['_id'], computerMonitor['place'])
        assert_that(computerMonitor['events'][0]).is_subset_of(locate)
