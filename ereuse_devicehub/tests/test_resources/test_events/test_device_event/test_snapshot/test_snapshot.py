import copy
import os
import uuid
from random import choice

from assertpy import assert_that
from bson import objectid
from pydash import pick

from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.tests.test_resources.test_events import TestEvent
from ereuse_devicehub.utils import Naming, coerce_type
from ereuse_devicehub.utils import NestedLookup


class TestSnapshot(TestEvent):
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
    SNAPSHOT_URL = '{}/{}'.format(TestEvent.DEVICE_EVENT, TestEvent.SNAPSHOT)

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
        events = self.post_snapshot_get_full_events(input_snapshot, num_of_events)
        self.assertLen(events, num_of_events)
        register = events[0]
        self.assertType(DeviceEventDomain.new_type('Register'), register)
        self.assertSimilarDevice(input_snapshot['device'], register['device'])
        device = self.get_and_check(self.DEVICES, item=register['device'])
        if 'hid' in device:
            assert_that(device['hid']).is_not_equal_to('dummy')
        if 'components' in input_snapshot:
            self.assertSimilarDevices(input_snapshot['components'], register['components'])
        # We do a snapshot again. We should receive a new snapshot without any event on it.
        if do_second_time_snapshot:
            snapshot = self.post_and_check('{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), input_snapshot)
            self.assertLen(snapshot['events'], num_of_events - 1)
        return register['device']

    def add_remove(self, input_snapshot):
        component = choice(input_snapshot['components'])
        while True:
            ignore_fields = self.app.config['DOMAIN'][Naming.resource(component['@type'])]['etag_ignore_fields']
            key = choice(list(component.keys()))
            if key not in ignore_fields:
                break
        if type(component[key]) is int or type(component[key]) is float:
            component[key] += 10
        elif type(component[key]) is str:
            import uuid
            component[key] = uuid.uuid4().hex[:6].upper()
        self.post_snapshot_get_full_events(input_snapshot, 3)

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

    def test_snapshot_pc_then_register_component(self):
        """
        Snapshots a computer and then snapshots three non-existing components inside.

        The first component has HID, the second has not, and the third is a hard-drive with an erasure and a test
        events.
        """
        snapshot = self.get_fixture(self.SNAPSHOT, 'snapshot-simple')
        computer_id = self.creation(snapshot)
        snapshot_components_fixture = self.get_fixture(self.SNAPSHOT, 'snapshot-simple-components')
        snapshot_components = self.post_and_check(self.SNAPSHOT_URL, snapshot_components_fixture)
        computer = self.get_and_check(self.DEVICES, item=computer_id)
        # We check that the parent contains the components
        assert_that(computer['components']).contains(*snapshot_components['components'])
        # And that the components contain the parent
        components = [self.get_and_check(self.DEVICES, item=_id) for _id in snapshot_components['components']]
        assert_that(components).extracting('parent').contains_only(computer_id)

        # We check the same in events
        events = [self.get_and_check(self.EVENTS, item=_id) for _id in snapshot_components['events']]
        # The expected events have been created (apart from the Snapshot)...
        assert_that(events).extracting('@type').is_equal_to(
            ['devices:Register', 'devices:EraseBasic', 'devices:TestHardDrive'])
        # ...and have a reference to the computer parent device
        assert_that(events[0]['device']).contains('1')
        assert_that(events[1:]).extracting('parent').contains_only('1')

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

    def test_hid_vs_id(self):
        """
        Tests a second-time snapshot when there is conflict in hid/_id:
        hid equals to one device but _id equals to another.
        """
        vostro = self.get_fixture(self.SNAPSHOT, 'vostro')
        # We snapshot twice -> ok
        vostro_id = self.creation(vostro, 2)
        # If we set the id to vostro in vostro everything is ok
        # We could say we have a redundancy of ids
        vostro['device']['_id'] = vostro_id
        self.post_and_check(self.SNAPSHOT_URL, vostro)
        # Let's create another device
        vaio_id = self.creation(self.get_fixture(self.SNAPSHOT, 'vaio'))
        # Let's set the _id of vostro to vaio (for example because the user wrote misspelled it)
        # We get 'hid' as we can compute it. The device of the hid != device of the _id so the system
        # does not allow registering it
        vostro['device']['_id'] = vaio_id
        result, status = self.post(self.SNAPSHOT_URL, vostro)
        self.assert422(status)
        # Note that the unique id list the system checks against is a set, so the order where
        # the unique fields are checked is random. This means that depending on execution, one error
        # will be raised before the other, having to check two possible scenarios
        error1 = {'_issues': {'hid': 'This ID identifies the device 1 but the _id identifies the device 15'}}
        error2 = {'_issues': {'_id': 'This ID identifies the device 15 but the hid identifies the device 1'}}
        if 'hid' in result['_issues']:
            assert_that(result).is_equal_to(error1)
        else:
            assert_that(result).is_equal_to(error2)

    def test_uids(self):
        """
        Users can send snapshots with stating only one uid; like only the RID, the _id, the HID (S/N, model, man.)...

        The system should handle this snapshots with grace. Note that this does not apply in Workbench, as workbench
        always send all the uid info as possible.

        This system tries this behaviour.
        """
        snapshot = self.get_fixture(self.SNAPSHOT, 'monitor')
        _id = self.creation(snapshot, self.get_num_events(snapshot))
        snapshot['device']['rid'] = 'rid1'
        self.post_and_check(self.SNAPSHOT_URL, snapshot)
        monitor = self.get_and_check(self.DEVICES, item=_id)
        assert_that(monitor).has_rid('rid1')
        # Let's remove a field of the device, like the S/N, so it cannot generate HID
        # The system should be able to identify it with another uid, like the RID
        serial_number = snapshot['device'].pop('serialNumber')
        self.post_and_check(self.SNAPSHOT_URL, snapshot)
        monitor = self.get_and_check(self.DEVICES, item=_id)
        assert_that(monitor).has_rid('rid1').has_serialNumber(serial_number)
        # Or by only the _id, of course
        del snapshot['device']['rid']
        snapshot['device']['_id'] = _id
        self.post_and_check(self.SNAPSHOT_URL, snapshot)
        monitor = self.get_and_check(self.DEVICES, item=_id)
        assert_that(monitor).has_rid('rid1').has_serialNumber(serial_number)

    def test_snapshot_real_devices(self):
        # todo the processor of mounted.json and xps13 generates the same hid, as S/N is 'To be filled...'
        for file_name in self.REAL_DEVICES:
            snapshot = self.get_fixture(self.SNAPSHOT, file_name)
            num_events = self.get_num_events(snapshot)
            self.creation(snapshot, num_events)

    def test_snapshot_2015_12_09(self, maximum: int = None, extra_fields_snapshot: dict = None):
        this_directory = os.path.dirname(os.path.realpath(__file__))
        file_directory = os.path.join(this_directory, 'resources', '2015-12-09')
        i = 0
        for filename in os.listdir(file_directory):
            if maximum is not None and i >= maximum:
                break
            if 'json' in filename:
                snapshot = self.get_json_from_file(filename, file_directory)
                snapshot.update(extra_fields_snapshot or {})
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
        snapshot, test_hd, _, first_snapshot, _, _, register = (self.get(self.EVENTS, '', event['_id'])[0] for event in
                                                                device['events'])
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

    def test_condition(self, maximum: int = None):
        condition = {
            'appearance': {'general': 'A'},
            'functionality': {'general': 'C'}
        }
        self.test_snapshot_2015_12_09(maximum or 5, {'condition': condition})

    def _test_giver(self, snapshot, account_email):
        device_id = self.creation(snapshot, 2, False)
        account, status = self.get(self.ACCOUNTS, '', account_email)
        self.assert200(status)
        # Let's see that the materialized snapshot contains the event
        device, _ = self.get(self.DEVICES, '', device_id)
        for event in device['events']:
            if event['@type'] == 'Snapshot':
                assert_that(event).contains_key('receiver')
                assert_that(event['from']).is_equal_to(account['_id'])
                assert_that(event['from']).is_type_of(objectid)

    def test_from_registered(self):
        """
            Tests that 'from' is set to the event.
        """
        snapshot = self.get_fixture(self.SNAPSHOT, 'vostro')
        account = {'email': 'r@r.com', 'name': 'R Registered', 'organization': 'R ORG', '@type': 'Account',
                   'databases': ['dht1']}
        account = self.post_and_check(self.ACCOUNTS, account)
        snapshot['from'] = account['_id']
        self._test_giver(snapshot, 'r@r.com')

    def test_from_unregistered(self):
        """
            Tests that 'unregisteredFrom' is set to the event.
        """
        snapshot = self.get_fixture(self.SNAPSHOT, 'vostro')
        snapshot['from'] = {
            'email': 'r@r.com',
            'name': 'R Unregistered',
            'organization': 'R ORG'
        }
        self._test_giver(snapshot, 'r@r.com')

    def test_nice(self):
        snapshot = self.get_fixture(self.SNAPSHOT, 'nice')
        self.creation(snapshot, self.get_num_events(snapshot))

    def test_703b6_place_account(self):
        """
        Tests that the account and place in snapshot are correctly created.
        """
        snapshot = self.get_fixture(self.SNAPSHOT, '703b6')
        snapshot['from'] = {
            'email': 'hello@hello.com'
        }
        snapshot['place'] = self.post_and_check(self.PLACES, self.get_fixture(self.PLACES, 'place'))['_id']
        num_events = self.get_num_events(snapshot)
        device_id = self.creation(snapshot, num_events)
        device, _ = self.get(self.DEVICES, '', device_id)
        assert_that(device['place']).is_equal_to(snapshot['place'])
        account, status = self.get(self.ACCOUNTS, '', 'hello@hello.com')
        self.assert200(status)

    def test_71a4_eepc_erasure_real(self):
        """
        Tests a device generated with DeviceInventoroy version 7.0.3 beta 6
        """
        snapshot = self.get_fixture(self.SNAPSHOT, '71a4 eee-pc erasure real')
        num_events = self.get_num_events(snapshot)
        return self.creation(snapshot, num_events)

    def test_import(self):
        snapshot = self.get_fixture(self.SNAPSHOT, '703b6')
        # Import a device means manually setting the _id and created (which is going to be _created and _updated)
        snapshot['device']['_id'] = '123456789'
        snapshot['created'] = '2013-04-02T20:40:20'
        num_events = self.get_num_events(snapshot)
        _, status = self.post('{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), snapshot)
        # Only 'superuser' accounts can do so
        self.assert422(status)
        # Let's make account a superuser so it can arbitrary set both fields
        self.set_superuser()
        device_id = self.creation(snapshot, num_events)
        # Let's check that created and the id have been set correctly
        # Any event that we created from this snapshot should have the same date
        register = self.get_first(self.EVENTS)
        assert_that(register['_created']).is_equal_to('2013-04-02T20:40:20')
        assert_that(register['_updated']).is_equal_to('2013-04-02T20:40:20')
        assert_that(register['device']).is_equal_to('123456789')
        # And the same for the device
        device, _ = self.get(self.DEVICES, '', device_id)
        assert_that(device['_created']).is_equal_to('2013-04-02T20:40:20')
        assert_that(device['_updated']).is_equal_to('2013-04-02T20:40:20')

    def test_none(self):
        snapshot = self.get_fixture(self.SNAPSHOT, '71a4 eee-pc erasure real')
        # Let's set one random (non hid) value to None
        snapshot['components'][0]['memory'] = None
        # Let's set a value needed for HID to none
        snapshot['components'][1]['serialNumber'] = None
        # And a HID for the device
        # Note that we will need to force creation for the device as we won't be able to generate HID
        snapshot['device']['model'] = None
        _, status = self.post('{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), snapshot)
        self.assert422(status)
        snapshot['device']['forceCreation'] = True
        # We do not call self._creation as self.seem_equal is going to fail due to the Nones
        _, status = self.post('{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), snapshot)
        self.assert201(status)

    def test_import_device(self):
        self.set_superuser()
        snapshot = self.get_fixture(self.SNAPSHOT, 'import')
        self.creation(snapshot, self.get_num_events(snapshot))

    def test_import_no_serial_number(self):
        """
        Only superusers should be able to insert devices without satisfying the 'requeriments'.
        """
        snapshot = self.get_fixture(self.SNAPSHOT, 'import-no-sn')
        _, status = self.post('{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), snapshot)
        self.assert422(status)
        self.set_superuser()
        self.creation(snapshot, self.get_num_events(snapshot))

    def test_uuid(self):
        """Tests the usage of _uuid field, not allowing two equal uuid to be inserted"""
        snapshot = self.get_fixture(self.SNAPSHOT, self.REAL_DEVICES[0])
        snapshot['_uuid'] = str(uuid.uuid4())  # Just a random uuid
        # Note we do not perform a second-time snapshot, as it would be illegal with the same 'uuid'
        self.creation(snapshot, self.get_num_events(snapshot), do_second_time_snapshot=False)
        # As we are going to see now
        _, status = self.post('{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), snapshot)
        self.assert422(status)

    def test_8a1(self):
        """Tests a full Snapshot made with DDI version 8a1"""
        snapshot = self.get_fixture(self.SNAPSHOT, '8a1')
        # uuid would make this illegal
        self.creation(snapshot, self.get_num_events(snapshot), do_second_time_snapshot=False)

    def test_8b1_with_pid_and_id(self):
        """
        The version 8a1 puts the pid in the snapshot and not the device (which is wrong), but we need
        to deal with it.
        """
        snapshot = self.get_fixture(self.SNAPSHOT, 'workbench-80a1-pid')
        placeholder = self.get_fixture('register', '1-placeholder')
        placeholder['device']['_id'] = snapshot['_id']
        self.post_and_check('{}/{}'.format(self.DEVICE_EVENT, 'register'), placeholder)
        result = self.post_and_check(self.SNAPSHOT_URL, snapshot)
        device = self.get_and_check(self.DEVICES, item=result['device'])
        assert_that(device).has_hid('asustek_computer_inc-8boaaq191999-1000h')
        assert_that(device).has_pid(snapshot['pid'])
        assert_that(device).has__id(snapshot['_id'])
        # Let's try a second snapshot, just in case
        snapshot['_uuid'] = str(uuid.uuid4())  # Let's change the uuid or we won't be able to submit it
        self.post_and_check(self.SNAPSHOT_URL, snapshot)

    def test_placeholder_snapshot_hid(self):
        """Tests that hid is correctly computed in placeholders."""
        placeholder = self.get_fixture('register', '1-placeholder')
        placeholder['device']['_id'] = '1192'
        self.post_and_check('{}/{}'.format(self.DEVICE_EVENT, 'register'), placeholder)
        snapshot = self.get_fixture(self.SNAPSHOT, 'lenovo-6072')
        result = self.post_and_check(self.SNAPSHOT_URL, snapshot)
        device = self.get_and_check(self.DEVICES, item=result['device'])
        assert_that(device).has_hid(DeviceDomain.hid(device['manufacturer'], device['serialNumber'], device['model']))

    def test_snapshot_software_old(self):
        """Tests snapshotSoftware"""
        # Old version
        snapshot = self.get_fixture(self.SNAPSHOT, self.REAL_DEVICES[0])
        snapshot['snapshotSoftware'] = 'DDI'
        self.creation(snapshot, self.get_num_events(snapshot))
        # New version
        snapshot = self.get_fixture(self.SNAPSHOT, self.REAL_DEVICES[1])
        snapshot['snapshotSoftware'] = 'Workbench'
        self.creation(snapshot, self.get_num_events(snapshot))

    def test_workbench_then_app(self):
        """
        When performing a Snapshot through the app there is no information about components. In Workbench,
        an empty components array (or None) equals to *this device has no components, remove them*, but with the App
        the message is just *I am not providing any info about the components*. The Workbench scenario is by default;
        this test ensures that the App scenario is well handled.
        """
        workbench = self.get_fixture(self.SNAPSHOT, 'vaio')
        workbench = self.post_snapshot(workbench)
        workbench = self.get_and_check(self.EVENTS, item=workbench['_id'])
        device_after_workbench = self.get_and_check(self.DEVICES, item=workbench['device'])
        components_after_workbench = [self.get_and_check(self.DEVICES, item=component_id) for component_id in
                                      device_after_workbench['components']]
        # Let's create our App Snapshot
        app = self.get_fixture(self.SNAPSHOT, 'vaio')
        app['snapshotSoftware'] = 'AndroidApp'  # This is how we differentiate snapshots from Workbench and App
        app['device'] = pick(device_after_workbench, 'serialNumber', 'manufacturer', 'model', '@type')
        del app['components']  # '[]' is set by default if this is None
        # The rest of values of Snapshot can be the same, they won't affect
        app = self.post_snapshot(app)
        app = self.get_and_check(self.EVENTS, item=app['_id'])
        device_after_app = self.get_and_check(self.DEVICES, item=app['device'])
        components_after_app = [self.get_and_check(self.DEVICES, item=component_id) for component_id in
                                device_after_app['components']]

        assert_that(device_after_app.pop('events')).contains(*device_after_workbench.pop('events'))
        assert_that(device_after_app).is_equal_to(device_after_workbench)

        for component_w, component_a in zip(components_after_workbench, components_after_app):
            assert_that(component_w.pop('events')).contains(*component_a.pop('events'))
            assert_that(component_w).is_equal_to(component_a)
