import os

from assertpy import assert_that
from passlib.handlers.sha2_crypt import sha256_crypt

from ereuse_devicehub.resources.event.device.migrate.settings import Migrate
from ereuse_devicehub.resources.event.device.register.settings import Register
from ereuse_devicehub.tests import TestBase
from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent
from ereuse_devicehub.utils import Naming


class TestMigrate(TestDeviceEvent):
    MIGRATE = 'migrate'
    MIGRATE_URL = '{}/{}'.format(TestDeviceEvent.DEVICE_EVENT, MIGRATE)

    @staticmethod
    def set_settings(settings):
        settings.DHT3_DBNAME = 'dht3_'
        settings.DHT4_DBNAME = 'dht4_'
        TestDeviceEvent.set_settings(settings)
        settings.DATABASES += 'dht3', 'dht4'

    def setUp(self, settings_file=None, url_converters=None):
        super().setUp(settings_file, url_converters)
        # Let's add another account
        self.db.accounts.insert(
            {
                'email': 'b@b.b',
                'password': sha256_crypt.encrypt('1234'),
                'role': 'admin',
                'token': 'TOKENB',
                'databases': self.app.config['DATABASES'][1],
                'defaultDatabase': self.app.config['DATABASES'][1],
                '@type': 'Account'
            }
        )
        self.token_b = super(TestBase, self).post('/login', {'email': 'b@b.b', 'password': '1234'})[0]['token']
        self.db2 = self.app.config['DATABASES'][1]  # 'dht2'
        self.db1 = self.app.config['DATABASES'][0]  # 'dht1'

    def test_migrate(self):
        """Tests a basic migrate of multiple devices, from one database (db1) to another database (db2)."""
        assert_that(self.domain).contains(Naming.resource('devices:Migrate'))
        fixture_migrate_to = self.get_fixture('migrate', 'migrate_to')
        fixture_migrate_to['devices'] = self.devices_id
        fixture_migrate_to['to']['database'] = self.db2
        migrate_db1_to_db2 = self.post_and_check('{}/{}'.format(self.DEVICE_EVENT, self.MIGRATE), fixture_migrate_to)
        migrate_db1_to_db2, _ = self.get(Migrate.resource_name, '', migrate_db1_to_db2['_id'])
        del fixture_migrate_to['to']  # to contains a new field
        assert_that(fixture_migrate_to).is_subset_of(migrate_db1_to_db2)
        assert_that(migrate_db1_to_db2['to']['url']).contains(migrate_db1_to_db2['to']['baseUrl'])
        # Le'ts see if the migrate in db2 is correct
        fixture_migrate_from = self.get_fixture('migrate', 'migrate_from')
        migrate_from_db1, status = self._get(migrate_db1_to_db2['to']['url'], self.token_b)
        self.assert200(status)
        assert_that(fixture_migrate_from).is_subset_of(migrate_from_db1)
        assert_that(migrate_from_db1['from']).contains(migrate_db1_to_db2['_links']['self']['href'])
        # Let's check that the devices in db2 are the same than in db1
        assert_that(migrate_from_db1).contains('devices')
        assert_that(migrate_from_db1['devices']).is_not_empty()
        devices_db1 = [self.get(self.DEVICES, '', device_id)[0] for device_id in self.devices_id]
        devices_db2 = [self.get(self.DEVICES, '', device_id, True, self.db2)[0] for device_id in
                       migrate_from_db1['devices']]
        self.assertSimilarDevices(devices_db1, devices_db2, True)

        # We should not be able to perform an event with one of those devices in db1
        patched_place = {
            '_id': self.place['_id'],
            '@type': 'Place',
            'devices': self.devices_id
        }
        _, status = self.patch('{}/{}'.format(self.PLACES, self.place['_id']), patched_place)
        # todo it should be 422 however eve's patch renders 400 if exception does not extend werkzeug's HTTPException
        self.assert400(status)
        del patched_place['devices']  # By removing the devices it should work (empty place)
        _, status = self.patch('{}/{}'.format(self.PLACES, self.place['_id']), patched_place)
        self.assert200(status)
        allocate = self.get_fixture('allocate', 'allocate')  # Let's post another event
        allocate['to'] = self.get_first('accounts')['_id']
        allocate['devices'] = self.devices_id
        _, status = self.post(self.DEVICE_EVENT + '/allocate', allocate)
        self.assert422(status)
        # Let's get the devices in the actual state to use later
        devices_in_db1 = [self.get(self.DEVICES, '', device_id)[0] for device_id in self.devices_id]
        number_devices_in_db1 = len(self.get(self.DEVICES)[0])

        # Let's perform the same but in db2
        # Note that we will need to create the place in db2
        place = self.get_fixture(self.PLACES, 'place')
        place['devices'] = self.devices_id
        place_in_db2, status = self._post('{}/{}'.format(self.db2, self.PLACES), place, self.token_b)
        self.assert201(status)

        # Let's perform a Migrate back to db1, moving the devices to db1
        fixture_migrate_to = self.get_fixture('migrate', 'migrate_to')
        fixture_migrate_to['to']['database'] = self.db1
        fixture_migrate_to['devices'] = self.devices_id
        fixture_migrate_to['label'] = 'Migrate back to db1'
        url = '{}/{}/{}'.format(self.db2, self.DEVICE_EVENT, self.MIGRATE)
        migrate_db2_to_db1, status = self._post(url, fixture_migrate_to, self.token_b)
        self.assert201(status)
        migrate_db2_to_db1, _ = self._get('{}/{}/{}'.format(self.db2, self.EVENTS, migrate_db2_to_db1['_id']),
                                          self.token_b)
        del fixture_migrate_to['to']  # to contains a new field
        assert_that(fixture_migrate_to).is_subset_of(migrate_db2_to_db1)
        assert_that(migrate_db2_to_db1['to']['url']).contains(migrate_db2_to_db1['to']['baseUrl'])
        # Let's check that the devices in db1 only have one more event: the migrate (no Add, Register...)
        for device in devices_in_db1:
            device_db1_after_migrate, _ = self.get(self.DEVICES, '?embedded={"events":1}', device['_id'])
            assert_that(device_db1_after_migrate['events']).is_length(len(device['events']) + 1)
            # The last event is the resulting migrate (the one with 'from') executed in db1 by migrate_db2_to_db1
            migrate_from_db2, _ = self._get(migrate_db2_to_db1['to']['url'], self.token)
            assert_that(device_db1_after_migrate['events'][0]['_id']).is_equal_to(migrate_from_db2['_id'])
            # The one before is the migrate with 'to' called in db1 migrate_db1_to_db2
            assert_that(device_db1_after_migrate['events'][1]['_id']).is_equal_to(migrate_db1_to_db2['_id'])
            # And the first event is always a register
            assert_that(device_db1_after_migrate['events'][-1]['@type']).is_equal_to(Register.type_name)
        # Let's check that there are exactly the same number of devices now than before, and in db2
        # Note that the system can create a new device if there is no HID, but by issuing the URL
        # with the device, the system should be able to identify a device with the `URL in sameAs`
        number_devices_in_db1_after = len(self.get(self.DEVICES)[0])
        assert_that(number_devices_in_db1).is_equal_to(number_devices_in_db1_after)
        number_devices_in_db2 = len(self.get(self.DEVICES, '', None, True, self.db2)[0])
        assert_that(number_devices_in_db1).is_equal_to(number_devices_in_db2)

        # Finally, let's perform an event with the devices in db1
        _, status = self.patch('{}/{}'.format(self.PLACES, self.place['_id']), patched_place)
        self.assert200(status)
        # And to db2: devices are not here anymore so:
        # a) they have been automatically removed from their place in db2
        place_in_db2, status = self._get('{}/{}/{}'.format(self.db2, self.PLACES, place_in_db2['_id']), self.token_b)
        self.assert200(status)
        # assert_that(place_in_db2).does_not_contain('devices')
        assert_that(place_in_db2['devices']).does_not_contain(*[device['_id'] for device in devices_db2])
        # b) you cannot POST/PUT/PATCH/DELETE anything with a reference to those devices
        new_patch_for_place_in_db2 = {
            '@type': 'Place',
            'devices': self.devices_id
        }
        url = '{}/{}/{}'.format(self.db2, self.PLACES, place_in_db2['_id'])
        _, status = self._patch(url, new_patch_for_place_in_db2, self.token_b)
        self.assert400(status)

    def add_accounts_dht3and4(self):
        self.db.accounts.insert(
            {
                'email': 'c@c.c',
                'password': sha256_crypt.encrypt('1234'),
                'role': 'admin',
                'token': 'TOKENC',
                'databases': self.app.config['DATABASES'][2],
                'defaultDatabase': self.app.config['DATABASES'][2],
                '@type': 'Account'
            }
        )
        self.token_c = super(TestBase, self).post('/login', {'email': 'c@c.c', 'password': '1234'})[0]['token']
        self.db.accounts.insert(
            {
                'email': 'd@d.d',
                'password': sha256_crypt.encrypt('1234'),
                'role': 'admin',
                'token': 'TOKEND',
                'databases': self.app.config['DATABASES'][3],
                'defaultDatabase': self.app.config['DATABASES'][3],
                '@type': 'Account'
            }
        )
        self.token_d = super(TestBase, self).post('/login', {'email': 'd@d.d', 'password': '1234'})[0]['token']
        self.db3 = self.app.config['DATABASES'][2]  # 'dht3'
        self.db4 = self.app.config['DATABASES'][3]  # 'dht4'

    def test_migrate_placeholder(self):
        """
        Creates 15 placeholders from db1 and moves them to db2-4, receiving 5 each. Then, they discover the devices.
        """
        self.add_accounts_dht3and4()
        # Let's get 15 snapshots that we will use to 'discover' the devices later
        full_snapshots = []
        this_directory = os.path.dirname(os.path.realpath(__file__))
        file_directory = os.path.join(this_directory, '..', 'test_snapshot', 'resources', '2015-12-09')
        for i, filename in zip(range(0, 15), os.listdir(file_directory)):
            if 'json' in filename:
                full_snapshots.append(self.get_json_from_file(filename, file_directory))

        devices_id = []
        for i in range(1, 15):
            placeholder = self.get_fixture('register', '1-placeholder')
            event = self.post_and_check('{}/{}'.format(self.DEVICE_EVENT, 'register'), placeholder)
            devices_id.append(event['device'])
        tokens = self.token_b, self.token_c, self.token_d
        for db, token, i in zip(self.app.config['DATABASES'][1:], tokens, range(0, 3)):
            f_migrate_to = self.get_fixture('migrate', 'migrate_to')
            f_migrate_to['devices'] = devices_id[(i * 5):(i * 5 + 5)]
            f_migrate_to['to']['database'] = db
            migrate_to = self.post_and_check(self.MIGRATE_URL, f_migrate_to)
            migrate_other_db, status = self._get(migrate_to['to']['url'], token)
            self.assert200(status)
            for device_id in migrate_other_db['devices']:
                full_snapshot = full_snapshots.pop(-1)
                full_snapshot['device']['_id'] = device_id
                _, status = self._post('{}/{}/{}'.format(db, self.DEVICE_EVENT, self.SNAPSHOT), full_snapshot, token)
                self.assert201(status)
