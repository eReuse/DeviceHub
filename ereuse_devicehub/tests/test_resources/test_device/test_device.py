from assertpy import assert_that

from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.tests import TestStandard


class TestDevice(TestStandard):
    def setUp(self, settings_file=None, url_converters=None):
        super().setUp(settings_file, url_converters)
        self.place = self.post_fixture(self.PLACES, self.PLACES, 'place')

    def test_materializations_events(self):
        """
        Tests materializations related to events.
        :return:
        """
        # Let's check POST
        devices = self.get_fixtures_computers()
        vaio, _ = self.get(self.DEVICES, '', devices[0])
        account_id = str(self.account['_id'])
        materialized = [
            {'@type': DeviceEventDomain.new_type('Snapshot'), 'secured': False, 'byUser': account_id,
             'incidence': False},
            {'@type': DeviceEventDomain.new_type('Register'), 'secured': False, 'byUser': account_id,
             'incidence': False},
        ]
        fields = {'@type', '_id', 'byUser', 'incidence', 'secured', '_updated'}
        self.assertIn('events', vaio)
        i = 0
        for event in vaio['events']:
            # Order needs to be preserved
            assert_that(materialized[i]).is_subset_of(event)
            assert_that(set(event.keys())).is_equal_to(fields)
            i += 1
