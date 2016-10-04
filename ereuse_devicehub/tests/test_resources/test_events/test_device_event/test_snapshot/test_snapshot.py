import copy
import os
from pprint import pprint
from random import choice

from assertpy import assert_that
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.tests import TestStandard
from ereuse_devicehub.utils import Naming, coerce_type
from ereuse_devicehub.utils import NestedLookup


class TestSnapshot(TestStandard):
    DUMMY_DEVICES = (
        '1_1_Register_one_device_with_components',
        '1 - 2 - Register second device with components of first',
        '1 - 3 - Register 1-1 but removing motherboard moving processor from 1-2 to 1-1',
        '1 - 4 - Register 1-1 but removing processor (which ended again in 1-1) and adding graphicCard'
    )
    REAL_DEVICES = (
        'vostro', 'vaio', 'xps13'
    )
    RESOURCES_PATH = 'test_events/test_snapshot/resources/'

    def assertSimilarDevice(self, input_device: dict or str, created_device: dict or str):
        """
        Checks that the createdDevice is the same as the input one, removing computed values as hid... It uses etag.
        :param input_device Input device needs all the float values to have, by default, ".0", or it won't work
        """
        # todo make sure .0 doesn't crush in real program
        parsed_device = self.parse_device(input_device)
        with self.app.app_context():
            from ereuse_devicehub.resources.device.domain import DeviceDomain
            self.assertTrue(
                DeviceDomain.seem_equal(self.full(self.DEVICES, parsed_device),
                                        self.full(self.DEVICES, created_device)))

    def assertSimilarDevices(self, input_devices: list, created_devices: list, same_amount_of_devices=False):
        """
        Every created_device device must seem equal (same fields, except computed ones as hid...) as one of the input devices.

        There must be one input device per created device.
        :param input_devices:
        :param created_devices:
        :param same_amount_of_devices: bool Force to both lists to have the same amount of devices
        :return:
        """
        if same_amount_of_devices:
            self.assertEqual(len(input_devices), len(created_devices))
        for created_device in created_devices:
            found = False
            i = 0
            while not found and i < len(input_devices):
                try:
                    self.assertSimilarDevice(input_devices[i], created_device)
                    found = True
                except AssertionError:
                    pass
                i += 1
            self.assertTrue(found)

    def post_snapshot(self, input_snapshot):
        return self.post_and_check('{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), input_snapshot)

    def post_snapshot_get_full_events(self, input_snapshot, number_of_events_to_assert):
        snapshot = self.post_snapshot(copy.deepcopy(input_snapshot))
        self.assertEqual(len(snapshot['events']), number_of_events_to_assert)
        events = []
        for event_id in snapshot['events']:
            event, status_code = self.get('events', '', event_id)
            self.assert200(status_code)
            events.append(event)
        return events

    def creation(self, input_snapshot: dict, num_of_events: int = 1, do_second_time_snapshot=True) -> str:
        pprint("1st time snapshot:")
        events = self.post_snapshot_get_full_events(input_snapshot, num_of_events)
        self.assertLen(events, num_of_events)
        register = events[0]
        self.assertType(DeviceEventDomain.new_type('Register'), register)
        self.assertSimilarDevice(input_snapshot['device'], register['device'])
        if 'components' in input_snapshot:
            self.assertSimilarDevices(input_snapshot['components'], register['components'])
        # We do a snapshot again. We should receive a new snapshot without any event on it.
        if do_second_time_snapshot:
            pprint("2nd time snapshot:")
            snapshot, status_code = self.post('{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), input_snapshot)
            self.assert201(status_code)
            self.assertLen(snapshot['events'], num_of_events - 1)
        return register['device']

    def add_remove(self, input_snapshot):
        component = choice(input_snapshot['components'])
        found = False
        while not found:
            ignore_fields = self.app.config['DOMAIN'][Naming.resource(component['@type'])]['etag_ignore_fields']
            key = choice(list(component.keys()))
            found = key not in ignore_fields
        if type(component[key]) is int or type(component[key]) is float:
            component[key] += 10
        elif type(component[key]) is str:
            import uuid
            component[key] = uuid.uuid4().hex[:6].upper()
        events = self.post_snapshot_get_full_events(input_snapshot, 3)

    @staticmethod
    def get_num_events(snapshot):
        """
        Get the num of events a snapshot is going to produce, by knowing how many tests and erasures are in there.

        todo: compute add/Remove and other events, not just tests.
        :param snapshot:
        :return:
        """
        values = NestedLookup(snapshot, [], NestedLookup.key_equality_factory('test'))
        values += NestedLookup(snapshot, [], NestedLookup.key_equality_factory('erasure'))
        return len(values) + 1  # 1 == register event itself

    def test_add_remove(self):
        # todo create add/remove test with components and computers without hid
        # todo Check that the type of events generated are the correct ones
        folder = 'add_remove'
        snapshots = []
        for dummy_device in self.DUMMY_DEVICES:
            snapshots.append(self.get_fixture(folder, dummy_device))
        # We add the first device (2 times)
        self.creation(snapshots[0], self.get_num_events(snapshots[0]))
        # We register a new device, which has the processor of the first one
        # We have created 3 events (apart from the snapshot itself): Register, 1 Add and 1 Remove
        self.post_snapshot_get_full_events(snapshots[1], 3)
        # We register the first device again, but removing motherboard and moving processor from the second device
        # to the first. We have created 1 Add, 2 Remove (1. motherboard, 2. processor from second device)
        self.post_snapshot_get_full_events(snapshots[2], 3)
        # We register the first device but without the processor and adding a graphic card
        # We have created 1 Remove, 1 Add
        self.post_snapshot_get_full_events(snapshots[3], 2)

    def _test_snapshot_register_vostro(self):
        """
        Same as `test_snapshot_register_easy` however with real devices (fake serials), with all the risks that takes.
        :return:
        """
        self.creation(self.get_json_from_file(self.RESOURCES_PATH + 'vostro.json'), 2)

    def _test_snapshot_register_vaio(self):
        """
        Same as `test_snapshot_register_easy` however with real devices (fake serials), with all the risks that takes.
        :return:
        """
        self.creation(self.get_json_from_file(self.RESOURCES_PATH + self.REAL_DEVICES[1]))

    def _test_snapshot_register_dellxps(self):
        """
        Same as `test_snapshot_register_easy` however with real devices (fake serials), with all the risks that takes.
        :return:
        """
        self.creation(self.get_json_from_file(self.RESOURCES_PATH + self.REAL_DEVICES[2]))

    def test_snapshot_no_hid(self):
        """
        Tries a snapshot which's device has no hid, neither some components.

        The tests validates the process the process of inserting a device without hid.
        :return:
        """
        snapshot = self.get_fixture(self.SNAPSHOT, 'mounted')
        try:
            # Let's try first a simple snapshot
            self.post_snapshot(snapshot)
        except AssertionError as e:
            if e.args[0] == '422 != 201' and 'NeedsId' in e.message['_issues']['_id'][0]:
                # The system tells us that it could not register the device because the device (computer) has no hid
                # We can tell the system that this device already exists, by specifying an '_id', or stating
                # that this is new. We say it is new:
                snapshot['device']['forceCreation'] = True
                # And we repeat the process
                self.creation(snapshot, self.get_num_events(snapshot), False)
                # All ok. We remove the forceCreation and repeat the process
                del snapshot['device']['forceCreation']
                try:
                    self.post_snapshot(snapshot)
                except AssertionError as k:
                    # The system asks again the same. This time we will say that the device is the first one
                    # by specifying the '_id' to '1'
                    if k.args[0] == '422 != 201' and 'NeedsId' in k.message['_issues']['_id'][0]:
                        snapshot['device']['_id'] = '1'
                        # The system now is going to recognize the device and it's components,
                        # thus causing no extra event, apart from the snapshot itself
                        self.post_snapshot_get_full_events(snapshot, 0)
                    else:
                        raise e
            else:
                raise e
        else:
            self.assertTrue(False)  # We shouldn't we here, let's raise something

    def test_snapshot_real_devices(self) -> list:
        # todo the processor of mounted.json and xps13 generates the same hid, as S/N is 'To be filled...'
        for file_name in self.REAL_DEVICES:
            snapshot = self.get_fixture(self.SNAPSHOT, file_name)
            num_events = self.get_num_events(snapshot)
            self.creation(snapshot, num_events)

    def test_snapshot_2015_12_09(self, maximum: int = None):
        this_directory = os.path.dirname(os.path.realpath(__file__))
        file_directory = os.path.join(this_directory, 'resources', '2015-12-09')
        i = 0
        for filename in os.listdir(file_directory):
            if maximum is not None and i >= maximum:
                break
            if 'json' in filename:
                pprint(filename)
                snapshot = self.get_json_from_file(filename, file_directory)
                num_events = self.get_num_events(snapshot)
                self.creation(snapshot, num_events)
                i += 1

    def test_benchmark(self):
        # todo add benchmark for processors (which is done in `test_erase_sectors`
        snapshot = self.get_fixture(self.SNAPSHOT, 'device_benchmark')
        device_id = self.creation(snapshot, self.get_num_events(snapshot))
        full_device, _ = self.get(self.DEVICES, '?embedded={"components": 1}', device_id)
        # Let's check that the benchmarks have been created correctly
        for component in full_device['components']:
            # benchmark is a writeonly value
            self.assertNotIn('benchmark', component)
            if component['@type'] in ('HardDrive', 'Processor'):
                self.assertIn('benchmarks', component)
                benchmark = next((c for c in snapshot['components'] if c['@type'] == component['@type']))['benchmark']
                # self.creation makes 2 post, so we will have 2 benchmarks that are exactly the same
                self.assertListEqual(component['benchmarks'], [benchmark, benchmark])

    def test_erase_sectors(self):
        """
        Tests EraseSectors.

        Inserts a device with BenchmarkProcessor and BenchmarkHardDrive.
        """
        self._test_erase_sectors('erase_sectors')

    def test_erase_sectors_many_steps(self):
        """
        The same as :func:`test_erase_sectors`, however with more sectors and different benchmarks.
        """
        self._test_erase_sectors('erase_sectors_steps')

    def _test_erase_sectors(self, fixture_name):
        snapshot = self.get_fixture(self.SNAPSHOT, fixture_name)
        # We do a Snapshot 2 times
        device_id = self.creation(snapshot, self.get_num_events(snapshot))
        full_device, _ = self.get(self.DEVICES, '?embedded={"components": 1}', device_id)
        found = False
        for component in full_device['components']:
            if 'erasures' in component:
                hard_drive, _ = self.get(self.DEVICES, '?embedded={"erasures":1}', component['_id'])
                # erasure is a writeonly value
                self.assertNotIn('erasure', hard_drive)
                # erasures must exist and contain an array with 2 erasures, which are the same
                coerce_type(snapshot)  # We add prefix to types in snapshot
                erasure = next((c for c in snapshot['components'] if
                                'serialNumber' in c and c['serialNumber'] == component['serialNumber']))['erasure']
                self.assertLen(hard_drive['erasures'], 2)
                assert_that(erasure).is_subset_of(hard_drive['erasures'][0])
                assert_that(erasure).is_subset_of(hard_drive['erasures'][1])
                found = True
        self.assertTrue(found, 'Any component has erasures!')

    def _test_signed(self):
        """
        The same as :func:`test_erase_sectors_many_steps`, but with a signed json.

        We just try to POST it one, we do not do a full stack of tests.
        """
        # todo get good public key
        raw_snapshot = self.get_fixture(self.SNAPSHOT, 'test_signed', False)
        self.post_snapshot(raw_snapshot)

    def test_703b6(self):
        """
        Tests a device generated with DeviceInventoroy version 7.0.3 beta 6
        """
        snapshot = self.get_fixture(self.SNAPSHOT, '703b6')
        num_events = self.get_num_events(snapshot)
        return self.creation(snapshot, num_events)

    def test_703b6_delete(self):
        """
        Tests deleting a full device, ensuring related events and components are deleted.
        """
        device_id = self.test_703b6()
        device, _ = self.get(self.DEVICES, '', device_id)
        # The materialization keeps events of the device and its components, we only get test_hd as an event
        # for a component, to try with it later; let's ignore the rest of events from components
        snapshot, test_hd, _, first_snapshot, _, _, register = (self.get(self.EVENTS, '', event['_id'])[0] for event in device['events'])
        register, erase, test = (self.get(self.EVENTS, '', event_id)[0] for event_id in
                                 self.get(self.EVENTS, '', first_snapshot['_id'])[0]['events'])
        # Let's try deleting NOT the Snapshot that created the device
        self.delete_and_check(self.DEVICE_EVENT + '/snapshot/' + snapshot['_id'])
        _, status = self.get(self.EVENTS, '', snapshot['_id'])
        self.assert404(status)
        # We can still get the device, as the device was created with the *first* snapshot (that called Register)
        _, status = self.get(self.DEVICES, '', device_id)
        self.assert200(status)
        # The same for any other event that was not generated because of this snapshot
        _, status = self.get(self.EVENTS, '', test['_id'])
        self.assert200(status)
        # Or any component
        _, status = self.get(self.DEVICES, '', device['components'][0])
        self.assert200(status)

        # Let's add again a new snapshot
        # Note that this will produce a Remove event as there are no components
        new_snapshot = self.post_snapshot({'@type': 'Snapshot', 'device': device})
        new_remove, status = self.get(self.EVENTS, '', new_snapshot['events'][0])
        self.assert200(status)

        # Now let's delete the device
        self.delete_and_check(self.DEVICES + '/' + device_id)
        # The first Snapshot should have deleted all events that were generated from it
        _, status = self.get(self.EVENTS, '', test['_id'])
        self.assert404(status)
        _, status = self.get(self.EVENTS, '', erase['_id'])
        self.assert404(status)
        _, status = self.get(self.EVENTS, '', register['_id'])
        self.assert404(status)

        # Deleting the register event should have led to deleting the device,
        _, status = self.get(self.DEVICES, '', device_id)
        self.assert404(status)
        # ...all the components that were created in that Register,
        for component_id in device:
            _, status = self.get(self.DEVICES, '', component_id)
            self.assert404(status)
        # ...and finally the new snapshot we created...
        _, status = self.get(self.EVENTS, '', new_snapshot['_id'])
        self.assert404(status)
        # ...with the Remove it triggered...
        _, status = self.get(self.EVENTS, '', new_remove['_id'])
        self.assert404(status)
        # ...and the events of the components
        _, status = self.get(self.EVENTS, '', test_hd['_id'])
        self.assert404(status)

    def test_computer_monitor(self):
        snapshot = self.get_fixture(self.SNAPSHOT, 'monitor')
        self.creation(snapshot, 1)  # Register only
