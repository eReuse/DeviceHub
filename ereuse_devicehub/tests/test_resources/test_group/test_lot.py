import copy

from assertpy import assert_that

from ereuse_devicehub.tests.test_resources.test_group import TestGroupBase


class TestLot(TestGroupBase):
    def test_schema(self):
        assert_that(self.domain).contains('lots')
        schema = self.domain['lots']['schema']
        assert_that(schema['@type']['allowed']).contains('Lot', 'InputLot', 'OutputLot')
        assert_that(self.domain[self.LOTS]['url']).is_equal_to('lots')
        assert_that(self.domain['input-lot']['url']).is_equal_to('lots/input-lot')
        assert_that(self.domain['output-lot']['url']).is_equal_to('lots/output-lot')

    def test_lot_with_devices(self):
        """CRUD of a lot adding and removing devices through all different methods"""
        # Let's create a lot with one device in it
        computers_id = self.get_fixtures_computers()
        lot = self.get_fixture(self.LOTS, 'lot')
        lot['label'] = 'lot1'
        lot['children'] = {'devices': computers_id[0:2]}
        lot_id = self.post_and_check(self.LOTS, lot)['_id']
        # Let's PATCH the lot
        patched_lot = {
            '@type': 'Lot',
            'children': {'devices': computers_id}
        }
        self.patch_and_check('{}/{}'.format(self.LOTS, lot_id), copy.deepcopy(patched_lot))
        for computer_id in computers_id:
            self.is_parent('lot1', self.LOTS, computer_id, self.DEVICES)

        # Let's just make another patch removing a device
        removed_device = patched_lot['children']['devices'].pop(-1)
        self.patch_and_check('{}/{}'.format(self.LOTS, lot_id), patched_lot)
        # All the computers except the last one are accounted
        for computer_id in computers_id[:-1]:
            self.is_parent('lot1', self.LOTS, computer_id, self.DEVICES)
        self.is_not_parent(lot_id, self.LOTS, removed_device, self.DEVICES)
        # Finally let's remove the entire lot; devices must loose their place
        self.delete_and_check('{}/{}'.format(self.LOTS, lot_id))
        for computer_id in computers_id:
            self.child_does_not_have_parent('lot1', self.LOTS, computer_id, self.DEVICES)

    def test_lot_moving_devices(self):
        """Creates two lots (input and output) and moves multiple devices from one to another"""

        # Let's try first with regular lots
        # Devices can be in regular lots and at the end devices will be in both lots
        input = self.get_fixture(self.LOTS, 'lot')
        input_label = input['label'] = 'lot1'
        input_id = self.post_and_check(self.LOTS, input)['_id']
        output = self.get_fixture(self.LOTS, 'lot')
        output_label = output['label'] = 'lot2'
        output_id = self.post_and_check(self.LOTS, output)['_id']
        computers_id = self.get_fixtures_computers()

        # Let's add the computers to the input lot
        patched_input = {'@type': 'InputLot', 'children': {'devices': computers_id}}
        self.patch_and_check('{}/{}'.format(self.LOTS, input_id), patched_input)
        for computer_id in computers_id:
            self.is_parent(input_label, self.LOTS, computer_id, self.DEVICES)

        # Let's add them to the output lot
        patched_output = {'@type': 'OutputLot', 'children': {'devices': computers_id}}
        self.patch_and_check('{}/{}'.format(self.LOTS, output_id), patched_output)
        for computer_id in computers_id:
            self.is_parent(output_label, self.LOTS, computer_id, self.DEVICES)
        # They are in the first lot too
        for computer_id in computers_id:
            self.is_parent(input_label, self.LOTS, computer_id, self.DEVICES)

            # And now with input/output lots
            # Devices can have only one input/output lot at the same time as parent
            # input = self.get_fixture(self.LOTS, 'input-lot')
            # input_label = input['label']
            # input_id = self.post_and_check(self.INPUT_LOT_URL, input_label)
            # output = self.get_fixture(self.LOTS, 'output-lot')
            # output_label = output['label']
            # output_id = self.post_and_check(self.OUTPUT_LOT_URL, output_label)
            # computers_id = self.get_fixtures_computers()

            # Let's add the computers to the input lot
            # patched_input = {'@type': 'InputLot', 'children': {'devices': computers_id}}
            # self.patch_and_check('{}/{}'.format(self.INPUT_LOT_URL, input_id), patched_input)
            # for computer_id in computers_id:
            #    self.is_parent(input_label, self.INPUT_LOT, computer_id, self.OUTPUT_LOT)

            # Let's add them to the output lot
            # patched_output = {'@type': 'OutputLot', 'children': {'devices': computers_id}}
            # self.patch_and_check('{}/{}'.format(self.OUTPUT_LOT_URL, output_id), patched_output)
            # for computer_id in computers_id:
            #    self.is_parent(output_label, self.INPUT_LOT, computer_id, self.OUTPUT_LOT)
            # They are not in the first lot
            # for computer_id in computers_id:
            # self.is_not_parent(input_label, self.INPUT_LOT, computer_id, self.OUTPUT_LOT)
