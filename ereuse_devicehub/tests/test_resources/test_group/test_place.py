import copy

from ereuse_devicehub.tests.test_resources.test_group import TestGroupBase


class TestPlace(TestGroupBase):
    def setUp(self, settings_file=None, url_converters=None):
        super(TestPlace, self).setUp(settings_file, url_converters)
        self.place = self.get_fixture(self.PLACES, 'place')

    def test_create_place_with_coordinates(self):
        self.post_and_check(self.PLACES, self.place)

    def test_place_with_devices(self):
        """
        CRUD of a place adding and removing devices through all the different methods (POST / PUT / PATCH).
        :return:
        """
        # Let's create a place with one device in it
        computers_id = self.get_fixtures_computers()
        self.place['devices'] = [computers_id[0]]
        place = self.post_and_check(self.PLACES, copy.deepcopy(self.place))
        self.device_and_group_contain_each_other(computers_id[0], place['_id'], self.PLACES, 'place')
        # Let's PATCH de place with the device 1 and 2
        patched_place = {
            '_id': place['_id'],
            '@type': 'Place',
            'devices': place['devices'] + computers_id[1:2]
        }
        self.patch_and_check('{}/{}'.format(self.PLACES, place['_id']), patched_place)
        # Now we have computers 0, 1 and 2
        for computer_id in computers_id[:2]:
            self.device_and_group_contain_each_other(computer_id, place['_id'], self.PLACES, 'place')
        # Let's PUT adding the last device
        place = copy.deepcopy(self.place)  # We do not want any readonly values
        place['_id'] = patched_place['_id']
        place['devices'] = computers_id
        self.put('{}/{}'.format(self.PLACES, place['_id']), place)
        for computer_id in computers_id:
            self.device_and_group_contain_each_other(computer_id, place['_id'], self.PLACES, 'place')
        # Now let's remove a device from the place
        del place['devices'][0]
        for computer_id in computers_id[1:]:
            self.device_and_group_contain_each_other(computer_id, place['_id'], self.PLACES, 'place')
        self.is_not_parent(place['_id'], self.PLACES, computers_id[0], self.DEVICES)
        # Finally, let's remove the entire place. Devices must loose their place
        self.delete_and_check('{}/{}'.format(self.PLACES, place['_id']))
        for computer_id in computers_id:
            self.is_not_parent(place['_id'], self.PLACES, computer_id, self.DEVICES)
