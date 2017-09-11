from assertpy import assert_that

from ereuse_devicehub.resources.device.component.hard_drive.settings import HardDrive
from ereuse_devicehub.resources.event.device.add.settings import Add
from ereuse_devicehub.resources.event.device.register.settings import Register
from ereuse_devicehub.resources.event.device.remove.settings import Remove
from ereuse_devicehub.resources.event.device.snapshot.settings import Snapshot
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
        materialized_events = [
            {'@type': Snapshot.type_name, 'secured': False, 'byUser': account_id, 'incidence': False},
            {'@type': Register.type_name, 'secured': False, 'byUser': account_id, 'incidence': False},
        ]
        fields = {'@type', '_id', 'byUser', 'incidence', 'secured', '_updated'}
        fields_snapshot = fields | {'snapshotSoftware'}
        self.assertIn('events', vaio)
        for event, materialized_event in zip(vaio['events'], materialized_events):
            assert_that(materialized_event).is_subset_of(event)  # Order needs to be preserved
            fields_to_check = fields if materialized_event['@type'] != 'devices:Snapshot' else fields_snapshot
            assert_that(set(event.keys())).is_equal_to(fields_to_check)

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
        self.post_201('{}/remove'.format(self.DEVICE_EVENT), remove)
        other_device, _ = self.get(self.DEVICES, '', devices[1])
        assert_that(other_device['totalHardDriveSize']).is_equal_to(other_device_total_hdd - hard_drive['size'])
        add = {'@type': Add.type_name, 'device': vaio['_id'], 'components': [hard_drive['_id']]}
        self.post_201('{}/add'.format(self.DEVICE_EVENT), add)
        vaio_after, _ = self.get(self.DEVICES, '', devices[0])
        assert_that(vaio_after['totalHardDriveSize']).is_equal_to(122104.3359375 + 15296.0 + hard_drive['size'])

    def test_delete(self):
        """Deletes a device."""
        snapshot = self.post_fixture(self.SNAPSHOT, '{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), 'vaio')
        device = self.get_200(self.DEVICES, item=snapshot['device'])
        _, status = self.delete(self.DEVICES, item=device['_id'])
        self.assert204(status)
        # Let's check that any event is there
        for event in device['events']:
            _, status = self.get(self.EVENTS, item=event['_id'])
            self.assert404(status)
