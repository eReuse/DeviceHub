import json
from random import choice

from assertpy import assert_that
from passlib.handlers.sha2_crypt import sha256_crypt
from pydash import every, pluck, py_
from werkzeug.datastructures import Headers

from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.event.device.reserve.settings import Reserve
from ereuse_devicehub.security.perms import ACCESS, PARTIAL_ACCESS, READ
from ereuse_devicehub.tests.test_resources.test_group import TestGroupBase


class TestSecurity(TestGroupBase):
    def setUp(self, settings_file=None, url_converters=None):
        super(TestSecurity, self).setUp(settings_file, url_converters)
        self.devices_id = self.get_fixtures_computers()
        self.db.accounts.insert_one(
            {
                'email': 'b@b.b',
                'password': sha256_crypt.hash('1234'),
                'role': Role.ADMIN,
                'token': 'TOKENB',
                'databases': {self.app.config['DATABASES'][1]: ACCESS},
                'defaultDatabase': self.app.config['DATABASES'][1],
                '@type': 'Account'
            }
        )
        self.account2 = self.login('b@b.b', '1234')
        self.token2 = self.account2['token']

    def test_credentials(self):
        """Checks accessing resources through authentication, supposing permissions are correct."""
        # We access to the private device without credentials
        _, status_code = self.get(self.DEVICES, '', self.devices_id[0], False)
        self.assert401(status_code)
        # We access to all the devices without credentials
        _, status_code = self.get(self.DEVICES, authorize=False)
        self.assert401(status_code)
        # We access to all the devices with credentials
        _, status_code = self.get(self.DEVICES, authorize=True)
        self.assert200(status_code)
        # We access to another item endpoint without credentials
        private_event = self.get_first(self.DEVICE_EVENT)
        _, status_code = self.get(self.DEVICE_EVENT, '', private_event['_id'], False)
        self.assert401(status_code)

    def test_get_resources(self):
        """Checks GETting resources chaning resource permissions"""
        # The default user we use in other tests has ADMIN permission, so we won't test those here
        # As ADMIN and OWNER are the same (ADMIN can change settings and share, but this is not implemented yet)
        # So we don't test OWNER neither
        # We created in setup an user with OWNER access to a second database
        # but no access to the first database
        # Let's create a lot and add all devices
        lot = self.get_fixture(self.LOTS, 'lot')
        computers_id_in_lot = self.devices_id[:2]
        computers_id_not_in_lot = self.devices_id[2:]
        lot['children'] = {'devices': computers_id_in_lot}
        lot = self.post_201(self.LOTS, lot)

        # Any OP with the second database (the one the account has OWN access) works...
        self.get_200(self.DEVICES, token=self.token2, db=self.db2)
        self.post_201(self.DEVICE_EVENT_SNAPSHOT, self.get_fixture(self.SNAPSHOT, '9'), token=self.token2,
                      db=self.db2)

        # But the account can't access to the first database (as it has not access at it)
        _, status = self.get(self.DEVICES, token=self.token2)
        self.assert401(status)
        _, status = self.post(self.DEVICE_EVENT_SNAPSHOT, self.get_fixture(self.SNAPSHOT, '9'), token=self.token2)
        self.assert401(status)
        # We can't get the lot
        _, status = self.get(self.LOTS, item=lot['_id'], token=self.token2)
        self.assert401(status)
        # Neither the devices inside
        where = {'_id': {'$in': computers_id_in_lot}}
        _, status = self.get(self.DEVICES, params={'where': json.dumps(where)}, token=self.token2)
        self.assert401(status)

        # Let's share the lot to the user
        lot_patch = {'@type': 'Lot', 'perms': [{'account': self.account2['_id'], 'perm': READ}]}  # We share the lot
        self.patch_200(self.LOTS, item=lot['_id'], data=lot_patch)

        # The user now has PARTIAL_ACCESS to its databases
        account2 = self.get_200(self.ACCOUNTS, item=self.account2['_id'], token=self.token2)
        assert_that(account2['databases']).has_dht1(PARTIAL_ACCESS)
        # and explicit shared access with
        shared = {'db': self.db1, '@type': 'Lot', 'label': 'Lot from User',
                  '_id': lot['_id'], 'baseUrl': self.app.config['BASE_URL_FOR_AGENTS']}
        assert_that(account2).has_shared([shared])

        # Now the user can GET the lot
        lot = self.get_200(self.LOTS, item=lot['_id'], token=self.token2)
        assert_that(lot).has_perms([{'account': self.account2['_id'], 'perm': READ}])
        assert_that(lot).has_sharedWith([self.account2['_id']])

        # And its inner devices
        computers_in_lot = self.get_200(self.DEVICES, params={'where': json.dumps(where)}, token=self.token2)
        assert_that(computers_in_lot['_items']).is_length(2)
        for device in computers_in_lot['_items']:
            assert_that(device['_id']).is_not_equal_to(computers_id_not_in_lot[0])
            # with its events
            self.get_200(self.EVENTS, params={'where': json.dumps({'_id': {'$in': pluck(device['events'], '_id')}})},
                         token=self.token2)
        # Let's try getting only one event
        self.get_200(self.EVENTS, item=choice(choice(computers_in_lot['_items'])['events'])['_id'])

        # But not other resources not in the lot
        where = {
            '$or': [
                {'ancestors': {'$elemMatch': {'@type': 'Lot', '_id': lot['_id']}}},
                {'ancestors': {'$elemMatch': {'lots': {'$elemMatch': {'$in': ['_id']}}}}}
            ]
        }
        devices_in_lot = self.get_200(self.DEVICES, params={'where': json.dumps(where)}, token=self.token2)['_items']
        all_devices = self.get_200(self.DEVICES, token=self.token2)['_items']
        # Note that in this case we won't get 401 when getting resources
        # We will only get those resources we can access to
        assert_that(all_devices).is_equal_to(devices_in_lot)
        # with their events
        events = self.get_200(self.EVENTS, token=self.token2)['_items']
        # We get all ids of the events of our devices and check that the are the same that the ones we take
        number_events = py_(all_devices).pluck('events').flatten().pluck('_id').uniq().value()
        assert_that(pluck(events, '_id')).contains_only(*number_events)

        # If the user tries to get a specific resource that does not have access to,
        # we will get 401
        _, status = self.get(self.DEVICES, item=choice(computers_id_not_in_lot), token=self.token2)
        self.assert401(status)

    def test_modifying_resources(self):
        """Tests that accounts with shared permissions cannot modify resources."""
        # We create a lot like in the test above
        lot = self.get_fixture(self.LOTS, 'lot')
        computers_id_in_lot = self.devices_id[:2]
        computers_id_not_in_lot = self.devices_id[2:]
        lot['children'] = {'devices': computers_id_in_lot}
        lot = self.post_201(self.LOTS, lot)
        # And share it to our test user (self.account2)
        lot_patch = {'@type': 'Lot', 'perms': [{'account': self.account2['_id'], 'perm': READ}]}
        self.patch_200(self.LOTS, item=lot['_id'], data=lot_patch)
        # account2 can access to it
        self.get_200(self.DEVICES, item=choice(computers_id_in_lot), token=self.token2)
        # but can't post to the database
        device = self.get_fixture(self.SNAPSHOT, '9')
        _, status = self.post(self.DEVICE_EVENT_SNAPSHOT, data=device, token=self.token2)
        self.assert401(status)
        # At the same time it can't PATCH any group, even the shared one
        lot_patch = {'@type': 'Lot', 'children': {'devices': lot['children']['devices'] + computers_id_not_in_lot}}
        _, status = self.patch(self.LOTS, item=lot['_id'], data=lot_patch, token=self.token2)
        self.assert401(status)
        # If we take the lot with the superuser this has not been modified
        lot = self.get_200(self.LOTS, item=lot['_id'])
        assert_that(lot).has_children({'devices': computers_id_in_lot})

    def test_move_resources(self):
        """Tests adding/removing resources and checking their permissions"""
        # Let's start by creating a lot with some devices, and sharing it to account2
        lot = self.get_fixture(self.LOTS, 'lot')
        lot['children'] = {'devices': self.devices_id}
        lot['perms'] = [{'account': self.account2['_id'], 'perm': READ}]
        lot = self.post_201(self.LOTS, lot)

        # Now we can access the lot and device
        lot = self.get_200(self.LOTS, item=lot['_id'], token=self.token2)
        assert_that(lot).has_children({'devices': self.devices_id})
        device = self.get_200(self.DEVICES, item=choice(self.devices_id), token=self.token2)
        assert_that({'@type': 'Lot', '_id': lot['_id']}).is_subset_of(device['ancestors'][0])

        # We remove some devices from the lot, so we can't access them
        removed_devices_id = self.devices_id[:2]
        devices_id_in_lot = self.devices_id[2:]

        lot_patch = {'@type': 'Lot', 'children': {'devices': devices_id_in_lot}}
        self.patch_200(self.LOTS, item=lot['_id'], data=lot_patch)
        lot = self.get_200(self.LOTS, item=lot['_id'], token=self.token2)
        assert_that(lot).has_perms([{'account': self.account2['_id'], 'perm': READ}])
        # We can access a device that is left in the lot
        device_in_lot = self.get_200(self.DEVICES, item=choice(devices_id_in_lot), token=self.token2)
        assert_that(device_in_lot['perms']).is_equal_to(lot['perms'])
        # But we can't access any removed from the lot
        _, status = self.get(self.DEVICES, item=choice(removed_devices_id), token=self.token2)
        self.assert401(status)
        # A removed device doesn't have the permission anymore
        removed_device = self.get_200(self.DEVICES, item=choice(removed_devices_id))
        assert_that(removed_device).has_perms([])
        # If we access all devices we only get the ones in the lot (and their components)
        devices = self.get_200(self.DEVICES, token=self.token2)
        is_device_in_lot = lambda d: {d['_id'], d.get('parent', None)}.intersection(set(devices_id_in_lot))
        assert_that(every(devices['_items'], is_device_in_lot)).is_true()

        # We add a package to the lot, accessing the package
        package = self.post_fixture(self.PACKAGES, self.PACKAGES, 'package')
        lot_patch['children']['packages'] = [package['_id']]
        self.patch_200(self.LOTS, item=lot['_id'], data=lot_patch)
        package = self.get_200(self.PACKAGES, item=package['_id'], token=self.token2)
        assert_that(package).has_perms([{'account': self.account2['_id'], 'perm': READ}])

        # We add the device to the package, accessing the device
        package_patch = {'@type': 'Package', 'children': {'devices': removed_devices_id}}
        self.patch_200(self.PACKAGES, item=package['_id'], data=package_patch)
        params = {'where': json.dumps({'_id': {'$in': removed_devices_id}})}
        devices = self.get_200(self.DEVICES, params=params, token=self.token2)['_items']
        assert_that(devices).is_length(2)
        # We can access its events
        self.get_200(self.EVENTS, item=choice(choice(devices)['events'])['_id'])
        # Let's access specifically one of the devices
        removed_device = self.get_200(self.DEVICES, item=choice(removed_devices_id), token=self.token2)

        # Note that we can still access the other devices
        devices_token2 = self.get_200(self.DEVICES, token=self.token2)
        devices = self.get_200(self.DEVICES)
        # The same number
        assert_that(devices_token2['_meta']['total']).is_equal_to(devices['_meta']['total'])

        # We explicitly remove permissions from the package
        package_patch = {'@type': 'Package', 'perms': []}
        self.patch_200(self.PACKAGES, item=package['_id'], data=package_patch)
        package = self.get_200(self.PACKAGES, item=package['_id'])
        assert_that(package).has_perms([])
        # We can't access the package, devices neither their events
        _, status = self.get(self.PACKAGES, item=package['_id'], token=self.token2)
        self.assert401(status)
        _, status = self.get(self.DEVICES, item=choice(removed_devices_id), token=self.token2)
        self.assert401(status)
        _, status = self.get(self.EVENTS, item=choice(removed_device['events'])['_id'], token=self.token2)
        self.assert401(status)
        # The only events we can take are from the devices_id_in_lot
        events = self.get_200(self.EVENTS, token=self.token2)['_items']
        assert_that(pluck(events, 'device')).contains_only(*devices_id_in_lot)

        params = {'where': json.dumps({'_id': {'$in': removed_devices_id}})}
        devices = self.get_200(self.DEVICES, params=params, token=self.token2)
        assert_that(devices['_items']).is_length(0)

        # Note that the package is still in the lot
        self.is_parent(lot['_id'], self.LOTS, package['_id'], self.PACKAGES)

        # Let's add permission again to the lot, so the package will inherit them again
        # For that we need to remove it from the lot and re-add it to the lot
        lot_patch = {'@type': 'Lot', 'perms': []}
        self.patch_200(self.LOTS, item=lot['_id'], data=lot_patch)
        lot_patch['perms'] = [{'account': self.account2['_id'], 'perm': READ}]
        self.patch_200(self.LOTS, item=lot['_id'], data=lot_patch)
        # We can access the lot, package and all devices
        self.get_200(self.LOTS, item=lot['_id'], token=self.token2)
        self.get_200(self.PACKAGES, item=package['_id'], token=self.token2)
        device = self.get_200(self.DEVICES, item=choice(removed_devices_id), token=self.token2)
        self.get_200(self.DEVICES, item=choice(device['components']), token=self.token2)
        device = self.get_200(self.DEVICES, item=choice(devices_id_in_lot), token=self.token2)
        self.get_200(self.DEVICES, item=choice(device['components']), token=self.token2)

        # Removing the package makes us not accessing neither package or device
        lot_patch = {'@type': 'Lot', 'children': {'packages': []}}
        self.patch_200(self.LOTS, item=lot['_id'], data=lot_patch)
        self.is_not_parent(lot['_id'], self.LOTS, package['_id'], self.PACKAGES)

        _, status = self.get(self.PACKAGES, item=package['_id'], token=self.token2)
        self.assert401(status)
        _, status = self.get(self.DEVICES, item=choice(removed_devices_id), token=self.token2)
        self.assert401(status)

        self.get_200(self.DEVICES, item=choice(devices_id_in_lot), token=self.token2)

    def test_performing_events(self):
        """
        Checks performing events and accessing them adding/removing permissions in devices and groups.
        Tests, in order:

        1. Perform Reserve to devices from a group when user has READ access to a group.
        2. Unable to perform Reserve to a mix of devices that user can and can't access (READ).
        3. Unable to perform Reserve to a mix of devices the user could access before but now it can't, because
           they were removed from the group.
        4. Getting two events when the user has READ access and can't access to some of the devices
           of the event; one event is from the user and the other from another user
        5. Unable to access an event where the user had READ access to some of the events, but not anymore.

        Note that when we say the user has READ access we assume that the user does not have explicit access to the
        database, otherwise READ access is useless.
        """
        lot = self.get_fixture(self.LOTS, 'lot')
        accessible_devices = self.devices_id[:2]
        non_accessible_devices = self.devices_id[2:]
        lot['children'] = {'devices': accessible_devices}
        lot['perms'] = [{'account': self.account2['_id'], 'perm': READ}]
        lot_id = self.post_201(self.LOTS, lot)['_id']

        # 1. Perform Reserve to devices from a group when user has READ access to a group
        # -------------------------------------------------------------------------------
        # account2 can reserve the devices it can access
        reserve = {'@type': 'devices:Reserve', 'devices': accessible_devices}
        reserve1_id = self.post_201(self.DEVICE_EVENT_RESERVE, reserve, token=self.token2)['_id']

        # but it can't if there are some devices it can't access
        reserve['devices'] = accessible_devices + non_accessible_devices
        _, status = self.post(self.DEVICE_EVENT_RESERVE, reserve, token=self.token2)
        self.assert401(status)

        # 2. Try to perform Reserve to a mix of devices that user can and can't access (READ)
        # -----------------------------------------------------------------------------------
        # If we remove one of the accessible devices from the lot
        new_non_accessible_device = accessible_devices.pop(0)
        lot['children'] = {'devices': accessible_devices}
        lot_patch = {'@type': 'Lot', 'children': {'devices': accessible_devices}}
        self.patch_200(self.LOTS, lot_patch, item=lot_id)

        # 3. Try to perform Reserve to a mix of devices the user could access before but now
        #    it can't, because they were removed from the group
        # ----------------------------------------------------------------------------------
        # account2 won't be able to reserve the device we removed, although it reserved it before
        reserve2 = {'@type': 'devices:Reserve', 'devices': accessible_devices + [new_non_accessible_device]}
        _, status = self.post(self.DEVICE_EVENT_RESERVE, reserve2, token=self.token2)
        self.assert401(status)

        # 4. Getting two events when the user has READ access and can't access to some of the devices
        #    of the event; one event is from the user and the other from another user
        # -------------------------------------------------------------------------------------------
        # account1 can reserve it without problems
        reserve2_id = self.post_201(self.DEVICE_EVENT_RESERVE, reserve2)['_id']

        # Account2 can get the first reserve and second reserve, as the user has access to some of its devices
        self.get_200(self.EVENTS, item=reserve1_id, token=self.token2)
        self.get_200(self.EVENTS, item=reserve2_id, token=self.token2)
        self.get_200(self.EVENTS, token=self.token2)

        # 5. Unable to access an event where the user had READ access to some of the events, but not anymore
        # --------------------------------------------------------------------------------------------------
        # But if we remove all devices from the lot (or we stop sharing the lot)
        # The account2 won't be able to access that event
        lot_patch = {'@type': 'Lot', 'children': {'devices': []}}
        self.patch_200(self.LOTS, item=lot_id, data=lot_patch)

        _, status = self.get(self.EVENTS, item=reserve1_id, token=self.token2)
        self.assert401(status)
        # The owner of course it can access the resource
        self.get_200(self.EVENTS, item=reserve1_id)

    def _test_unauthorized_sharing(self):
        # todo we will let sharing in a future update
        # Let's start by creating a lot with some devices, and sharing it to account2
        lot = self.get_fixture(self.LOTS, 'lot')
        lot['children'] = {'devices': self.devices_id}
        lot['perms'] = [{'account': self.account2['_id'], 'perm': READ}]
        lot = self.post_201(self.LOTS, lot)

        # Let's add a third account
        self.db.accounts.insert_one(
            {
                'email': 'c@c.c',
                'password': sha256_crypt.hash('1234'),
                'role': Role.ADMIN,
                'token': 'TOKENB',
                'databases': {self.app.config['DATABASES'][1]: ACCESS},
                'defaultDatabase': self.app.config['DATABASES'][1],
                '@type': 'Account'
            }
        )
        account3 = self.login('c@c.c', '1234')

        # Account 2 can't share to account 3 as account2 has not ADMIN perms
        lot_patch = {'@type': 'Lot', 'perms': [{'account': account3['_id'], 'perm': READ}]}
        _, status = self.patch(self.LOTS, item=lot['_id'], data=lot_patch)
        self.assert401(status)

        # Account 1 can't share to itself as account1 has already database perms
        lot_patch = {'@type': 'Lot', 'perms': [{'account': self.account['_id'], 'perm': READ}]}
        _, status = self.patch(self.LOTS, item=lot['_id'], data=lot_patch)
        self.assert401(status)

    def test_redirect_on_browser(self):
        """Tests HTTP redirection to DevicehubClient when client is a browser (e.g. accepts HTML)"""
        # We want all petitions with accept/html to be redirected to the following client
        self.app.config['CLIENT'] = 'http://foo-client.com'
        reserve = self.post_201(self.DEVICE_EVENT_RESERVE,
                                data={'@type': Reserve.type_name, 'devices': self.devices_id})
        headers = Headers()
        headers.add('Accept', 'text/html')  # This is how we detect a browser
        response = self.test_client.get('{}/{}/{}'.format(self.db1, self.DEVICE_EVENT_RESERVE, reserve['_id']),
                                        headers=headers)
        self.assert302(response.status_code)
        url = 'http://foo-client.com/inventories/{}/devices_reserve.{}'.format(self.db1, reserve['_id'])
        assert_that(response).has_location(url)
