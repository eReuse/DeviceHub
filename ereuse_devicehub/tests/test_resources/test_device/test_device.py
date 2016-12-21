from assertpy import assert_that

from ereuse_devicehub.resources.device.component.hard_drive.settings import HardDrive
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.device.add.settings import Add
from ereuse_devicehub.resources.event.device.remove.settings import Remove
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

    def test_computer_materialization_fields(self):
        devices = self.get_fixtures_computers()
        vaio, _ = self.get(self.DEVICES, '?embedded={"components":1}', devices[0])
        assert_that(vaio).contains('totalRamSize', 'totalHardDriveSize', 'processorModel')
        assert_that(vaio['totalRamSize']).is_equal_to(8192)
        assert_that(vaio['totalHardDriveSize']).is_equal_to(122104.3359375 + 15296.0)
        assert_that(vaio['processorModel']).is_equal_to('Intel(R) Core(TM) i5-3337U CPU @ 1.80GHz')
        other_device, _ = self.get(self.DEVICES, '?embedded={"components":1}', devices[1])
        other_device_total_hdd = other_device['totalHardDriveSize']
        hard_drive, *_ = [hdd for hdd in other_device['components'] if hdd['@type'] == HardDrive.type_name]
        remove = {'@type': Remove.type_name, 'device': other_device['_id'], 'components': [hard_drive['_id']]}
        self.post_and_check('{}/remove'.format(self.DEVICE_EVENT), remove)
        other_device, _ = self.get(self.DEVICES, '', devices[1])
        assert_that(other_device['totalHardDriveSize']).is_equal_to(other_device_total_hdd - hard_drive['size'])
        add = {'@type': Add.type_name, 'device': vaio['_id'], 'components': [hard_drive['_id']]}
        self.post_and_check('{}/add'.format(self.DEVICE_EVENT), add)
        vaio_after, _ = self.get(self.DEVICES, '', devices[0])
        assert_that(vaio_after['totalHardDriveSize']).is_equal_to(122104.3359375 + 15296.0 + hard_drive['size'])
