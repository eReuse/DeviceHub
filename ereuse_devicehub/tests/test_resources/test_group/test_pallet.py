from ereuse_devicehub.tests.test_resources.test_group import TestGroupBase


class TestPallet(TestGroupBase):
    def test_pallet(self):
        pallet = self.get_fixture('groups', 'pallet')
        pallet = self.post_201(self.PALLETS, pallet)
        # Add pallet to lot
        lot = self.get_fixture('groups', 'lot')
        lot['children']['pallets'] = [pallet['_id']]
        lot = self.post_201(self.LOTS, lot)
        self.is_parent(lot['_id'], self.LOTS, pallet['_id'], self.PALLETS)
