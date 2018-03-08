from ereuse_devicehub.tests.test_resources.test_group import TestGroupBase


class TestPallet(TestGroupBase):
    def test_pallet(self):
        pallet = self.post_201(self.PALLETS, self.get_fixture('groups', 'pallet'))
        pallet_2 = self.post_201(self.PALLETS, self.get_fixture('groups', 'pallet'))
        # Add pallet to lot
        lot = self.get_fixture('groups', 'lot')
        lot['children']['pallets'] = [pallet['_id']]
        lot = self.post_201(self.LOTS, lot)
        self.is_parent(lot['_id'], self.LOTS, pallet['_id'], self.PALLETS)
        # Add devices to pallet
        devices_id = self.get_fixtures_computers()
        pallet_1_patch = {'@type': 'Pallet', 'children': {'devices': devices_id}}
        self.patch_200('{}/{}'.format(self.PALLETS, pallet['_id']), pallet_1_patch)
        # Move devices to second pallet
        pallet_2_patch = {'@type': 'Pallet', 'children': {'devices': devices_id}}
        self.patch_200('{}/{}'.format(self.PALLETS, pallet_2['_id']), pallet_2_patch)
        # Devices are not in first pallet anymore
        for device_id in devices_id:
            self.is_not_parent(pallet['_id'], self.PALLETS, device_id, self.DEVICES)
            self.is_parent(pallet_2['_id'], self.PALLETS, device_id, self.DEVICES)
        # Remove devices from pallet
        pallet_2_patch = {'@type': 'Pallet', 'children': {'devices': devices_id[:2]}}
        self.patch_200('{}/{}'.format(self.PALLETS, pallet_2['_id']), pallet_2_patch)
        for device_id in devices_id[2:]:
            self.is_not_parent(pallet_2['_id'], self.PALLETS, device_id, self.DEVICES)
        for device_id in devices_id[:2]:
            self.is_parent(pallet_2['_id'], self.PALLETS, device_id, self.DEVICES)
        # Move all of them back to pallet 1
        pallet_1_patch = {'@type': 'Pallet', 'children': {'devices': devices_id}}
        self.patch_200('{}/{}'.format(self.PALLETS, pallet['_id']), pallet_1_patch)
        for device_id in devices_id:
            self.is_parent(pallet['_id'], self.PALLETS, device_id, self.DEVICES)
            self.is_not_parent(pallet_2['_id'], self.PALLETS, device_id, self.DEVICES)
