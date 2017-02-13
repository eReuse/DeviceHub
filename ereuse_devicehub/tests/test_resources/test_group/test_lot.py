import copy

from assertpy import assert_that

from ereuse_devicehub.tests.test_resources.test_group import TestGroupBase


class TestLot(TestGroupBase):
    LOT = 'lot'

    def test_schema(self):
        assert_that(self.domain).contains('lot')
        schema = self.domain['lot']['schema']
        assert_that(schema['@type']['allowed']).contains('Lot', 'InputLot', 'OutputLot')
        assert_that(self.domain['lot']['url']).is_equal_to('lots')

    def test_lot_with_devices(self):
        """CRUD of a lot adding and removing devices through all different methods"""
        # Let's create a lot with one device in it
        computers_id = self.get_fixtures_computers()
        lot = self.get_fixture(self.LOT, 'lot')
        lot['devices'] = computers_id[0:2]
        lot = self.post_and_check(self.LOT, copy.deepcopy(lot))
        # Let's PATCH the lot
        patched_lot = {
            '_id': lot['_id'],
            '@type': 'InputLot',
            'devices': lot['devices'] + computers_id[2:4]
        }
        self.patch_and_check('{}/{}'.format(self.LOT, lot['_id']), copy.deepcopy(patched_lot))
        # Now we have all computers (4)
        for computer_id in computers_id:
            self.device_and_group_contain_each_other(computer_id, lot['_id'], self.LOT, 'lots')

        # Let's just make another patch removing a device
        removed_device = patched_lot['devices'].pop(-1)
        self.patch_and_check('{}/{}'.format(self.LOT, lot['_id']), copy.deepcopy(patched_lot))
        # All the computers except the last one are accounted
        for computer_id in computers_id[:-1]:
            self.device_and_group_contain_each_other(computer_id, lot['_id'], self.LOT, 'lots')
        self.is_parent(lot['_id'], self.LOT, removed_device, self.DEVICES)
        # Finally let's remove the entire lot; devices must loose their place
        self.delete_and_check('{}/{}'.format(self.LOT, lot['_id']))
        for computer_id in computers_id:
            self.is_not_parent(lot['_id'], self.LOT, computer_id, self.DEVICES)

    def test_lot_place(self):
        """Tests introducing/removing lots in places"""
        # Let's add a lot in a place
        place = self.get_fixture(self.PLACES, 'place')
        place = self.post_and_check(self.PLACES, place)
        lot = self.get_fixture(self.LOT, 'lot')
        lot['parent'] = [place['label']]
        lot = self.post_and_check(self.LOT, lot)
        self.is_parent(place['label'], self.PLACES, lot['label'], self.LOT)

        # Let's remove the lot from the place
        lot = self.get_fixture(self.LOT, 'lot')
        self.patch_and_check('{}/{}'.format(self.LOT, lot['label']), copy.copy(lot))
        self.is_parent(place['label'], self.PLACES, lot['label'], self.LOT)

        # Let's add two lots in a place
        second_lot = self.get_fixture(self.LOT, 'lot')
        second_lot['label'] = 'Second lot'
        second_lot['parent'] = lot['parent'] = place['label']
        # First lot
        self.patch_and_check('{}/{}'.format(self.LOT, lot['label']), copy.copy(lot))
        self.is_parent(place['label'], self.PLACES, lot['label'], self.LOT)
        # Second lot
        self.post_and_check(self.LOT, copy.copy(second_lot))
        # Both lots are in
        self.is_parent(place['label'], self.PLACES, lot['label'], self.LOT)
        self.is_parent(place['label'], self.PLACES, second_lot['label'], self.LOT)
        # Let's remove the second lot
        del second_lot['parent']
        self.patch_and_check('{}/{}'.format(self.LOT, second_lot['label']), copy.copy(second_lot))
        self.is_not_parent(place['label'], self.PLACES, second_lot['label'], self.LOT)


    def test_lot_packages(self):
        """Tests introducing/removing packages and devices in lots"""
        # To start, let's add a lot to a place
        place = self.get_fixture(self.PLACES, 'place')
        self.post_and_check(self.PLACES, place)
        lot = self.get_fixture(self.LOT, 'lot')
        lot['parent'] = [place['label']]
        self.post_and_check(self.LOT, lot)

        # Now let's add the package to the lot
        package = self.get_fixture(self.PACKAGES, 'package')
        package['parent'] = lot['label']
        self.post_and_check(self.PACKAGES, package)







