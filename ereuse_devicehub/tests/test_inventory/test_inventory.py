from datetime import timedelta, datetime

from assertpy import assert_that

from ereuse_devicehub.tests import TestStandard


class TestInventory(TestStandard):
    def test_inventory(self):
        URL = self.DEVICE_EVENT + '/'
        # We create 4 computers
        devices_id = self.get_fixtures_computers()
        # 2 have been fully processed (ready or disposed)
        self.post_and_check(URL + 'ready', {'@type': 'devices:Ready', 'devices': [devices_id[0]]})
        self.post_and_check(URL + 'dispose', {'@type': 'devices:Dispose', 'devices': [devices_id[1]]})
        # One is given another event, but this is not a 'processed' one
        self.post_and_check(URL + 'to-repair', {'@type': 'devices:ToRepair', 'devices': [devices_id[2]]})
        # And the third device is not even half-processed and it was created a time ago
        with self.app.app_context():
            operation = {'$set': {'_created': datetime.today() - timedelta(weeks=2)}}
            self.app.data.pymongo('devices', self.db1.upper()).db.devices.update_one({'_id': devices_id[3]}, operation)
        # We create a device with a broken hdd
        computer_with_broken_hdd = self.get_fixture('snapshot', '8a1')
        computer_with_broken_hdd['components'][2]['erasure']['success'] = False
        self.post_and_check(URL + 'snapshot', computer_with_broken_hdd)
        # And three placeholder
        self.post_and_check('events/devices_register/placeholders?quantity=3', {})

        # The actual test
        result, status = self._get(self.db1 + '/inventory')
        self.assert200(status)
        assert_that(result).is_equal_to(
            {'devicesMoreThanWeekWithoutBeingProcessed': 1, 'hardDrivesWithErrors': 1, 'devicesNotFullyProcessed': 6,
             'placeholders': 3}
        )
