import random

from assertpy import assert_that
from ereuse_devicehub.resources.event.device.migrate.settings import Migrate
from ereuse_devicehub.resources.event.device.register.settings import Register
from ereuse_devicehub.tests import TestBase
from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent
from ereuse_devicehub.utils import Naming
from passlib.handlers.sha2_crypt import sha256_crypt


class TestMigrate(TestDeviceEvent):
    MIGRATE = 'migrate'

    def setUp(self, settings_file=None, url_converters=None):
        super().setUp(settings_file, url_converters)
        # Let's add another account
        self.db.accounts.insert(
            {
                'email': 'b@b.b',
                'password': sha256_crypt.encrypt('1234'),
                'role': 'admin',
                'token': 'FDAEWHPIOZMGU',
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
        # Let's get one device of db1 to use later
        choice = random.choice(self.devices_id)
        print('Device chosen: ' + choice)
        device_db1, _ = self.get(self.DEVICES, '', choice)
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
        url = '{}/{}/{}'.format(self.db2, self.DEVICE_EVENT, self.MIGRATE)
        migrate_db2_to_db1, status = self._post(url, fixture_migrate_to, self.token_b)
        migrate_db2_to_db1, _ = self._get('{}/{}/{}'.format(self.db2, self.EVENTS, migrate_db2_to_db1['_id']),
                                          self.token_b)
        self.assert201(status)
        del fixture_migrate_to['to']  # to contains a new field
        assert_that(fixture_migrate_to).is_subset_of(migrate_db2_to_db1)
        assert_that(migrate_db2_to_db1['to']['url']).contains(migrate_db2_to_db1['to']['baseUrl'])
        # Let's check that the device in db1 only has one more event: the migrate (no Add, Register...)
        device_db1_after_migrate, _ = self.get(self.DEVICES, '?embedded={"events":1}', device_db1['_id'])
        assert_that(device_db1_after_migrate['events']).is_length(len(device_db1['events']) + 1)
        # The last event is the resulting migrate (the one with 'from') executed in db1 by migrate_db2_to_db1
        migrate_from_db2, _ = self._get(migrate_db2_to_db1['to']['url'], self.token)
        assert_that(device_db1_after_migrate['events'][0]['_id']).is_equal_to(migrate_from_db2['_id'])
        # The one before is the migrate with 'to' called in db1 migrate_db1_to_db2
        assert_that(device_db1_after_migrate['events'][1]['_id']).is_equal_to(migrate_db1_to_db2['_id'])
        # And the first event is always a register
        assert_that(device_db1_after_migrate['events'][-1]['@type']).is_equal_to(Register.type_name)
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
