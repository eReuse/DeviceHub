import json

from pydash import pluck

from assertpy import assert_that
from ereuse_devicehub.resources.group.abstract.lot.incoming_lot.settings import IncomingLot
from ereuse_devicehub.tests import TestStandard


class TestDhOperators(TestStandard):
    def test_inside_lot(self):
        """Tests the operator dh$insideLot"""
        computers_id = self.get_fixtures_computers()
        pcs_in_lot = computers_id[0:2]
        pcs_outside_lot = computers_id[2:4]
        lot = self.get_fixture(self.GROUPS, 'lot')
        lot['children']['devices'] = pcs_in_lot
        lot = self.post_201(self.LOTS, data=lot)
        where = {'dh$insideLot': lot['_id']}
        computers = self.get_200(self.DEVICES, params={'where': json.dumps(where)})
        # Note it will contain computers + their components
        assert_that(pluck(computers['_items'], '_id')).does_not_contain(pcs_outside_lot)
        # Now let's add a parent Place to the lot and add one device to the new Place
        # We should get three devices when we query with the operator
        pc_in_place = pcs_outside_lot.pop(0)
        ancestor_lot = self.get_fixture(self.GROUPS, 'lot')
        ancestor_lot['@type'] = IncomingLot.type_name  # Just to try another inside Lot
        ancestor_lot['children']['devices'] = [pc_in_place]
        ancestor_lot = self.post_201(self.LOTS, data=ancestor_lot)
        where = {'dh$insideLot': ancestor_lot['_id']}
        computers = self.get_200(self.DEVICES, params={'where': json.dumps(where)})
        assert_that(pluck(computers['_items'], '_id')).does_not_contain(pcs_outside_lot)
