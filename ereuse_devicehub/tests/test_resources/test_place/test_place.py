import copy

from ereuse_devicehub.tests import TestStandard


class TestPlace(TestStandard):
    def setUp(self, settings_file=None, url_converters=None):
        super(TestPlace, self).setUp(settings_file, url_converters)
        self.place = self.get_fixture(self.PLACES, 'place')

    def device_and_place_do_not_contain_each_other(self, device_id, place_id):
        """
        Exactly opposite of :func:`device_and_place_contain_each_other`
        :param device_id:
        :param place_id:
        :return:
        """
        try:
            place, _ = self.get(self.PLACES, place_id)
            try:
                self.assertNotIn(device_id, place['devices'])
            except KeyError:
                pass
        except AssertionError:
            pass  # It is fine if the place does not exist
        device, _ = self.get(self.DEVICES, device_id)
        try:
            self.assertNotIn(place_id, device['place'])
        except KeyError:
            pass
        if 'components' in device:
            for component_id in device['components']:
                component, _ = self.get(self.DEVICES, component_id)
                try:
                    self.assertNotIn(place_id, component['place'])
                except KeyError:
                    pass

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
        self.device_and_place_contain_each_other(computers_id[0], place['_id'])
        # Let's PATCH de place with the device 1 and 2
        patched_place = {
            '_id': place['_id'],
            '@type': 'Place',
            'devices': place['devices'] + computers_id[1:2]
        }
        self.patch_and_check('{}/{}'.format(self.PLACES, place['_id']), patched_place)
        # Now we have computers 0, 1 and 2
        for computer_id in computers_id[:2]:
            self.device_and_place_contain_each_other(computer_id, place['_id'])
        # Let's PUT adding the last device
        place = copy.deepcopy(self.place)  # We do not want any readonly values
        place['_id'] = patched_place['_id']
        place['devices'] = computers_id
        self.put('{}/{}'.format(self.PLACES, place['_id']), place)
        for computer_id in computers_id:
            self.device_and_place_contain_each_other(computer_id, place['_id'])
        # Now let's remove a device from the place
        del place['devices'][0]
        for computer_id in computers_id[1:]:
            self.device_and_place_contain_each_other(computer_id, place['_id'])
        self.device_and_place_do_not_contain_each_other(computers_id[0], place['_id'])
        # Finally, let's remove the entire place. Devices must loose their place
        self.delete('{}/{}'.format(self.PLACES, place['_id']))
        for computer_id in computers_id:
            self.device_and_place_do_not_contain_each_other(computer_id, place['_id'])
