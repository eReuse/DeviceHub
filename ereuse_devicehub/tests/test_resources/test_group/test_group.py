from ereuse_devicehub.tests.test_resources.test_group import TestGroupBase


class TestGroup(TestGroupBase):
    def test_add(self):
        package1 = self.get_fixture(self.PACKAGES, 'package')
        package1['label'] = 'package1'
        _id = self.post_and_check(self.PACKAGES, package1)['_id']
        _, status = self._get('{}/packages/{}'.format(self.db1, _id), token=self.token)
        self.assert200(status)

        _, status = self._get('{}/packages/package1'.format(self.db1), token=self.token)
        self.assert200(status)

    def test_group_full(self):
        """
            Generates a full hierarchy of groups and devices, performing the CRUD of operations, adding
            and removing different types of children with different types of groups.

            The idea is to represent this and then play with it:
                        Place1
                  _______/  \_____________
                 /     |           \__    \
                /      |              \    \
             Place2 Place3      Lot4 Lot5  |
           !!  |         \         \  / \__|
             Lot1_______  \        Lot3    |
               |        \  \        |  \___\
             Package1    \  \_____  |       \
               |    \___  \       \ |        \ Place4
             Device1   Package2   Package3    \
                          |         |         |
                       Device2    Device3  Device4
        """
        device1_id, device2_id, device3_id, device4_id = self.get_fixtures_computers()
        # Let's start with
        # Package1
        #    |
        # Device1
        package1 = self.get_fixture(self.PACKAGES, 'package')
        package1['label'] = 'package1'
        package1['children'] = {'devices': [device1_id]}
        package1_id = self.post_and_check(self.PACKAGES, package1)['_id']
        self.is_parent('package1', self.PACKAGES, device1_id, self.DEVICES)
        # Let's try to remove it
        package1_patch = {'@type': 'Package', 'children': {'devices': []}}
        self.patch_and_check('{}/{}'.format(self.PACKAGES, package1_id), package1_patch)
        self.is_not_parent('package1', self.PACKAGES, device1_id, self.DEVICES)
        # Let's add it again
        package1_patch['children']['devices'] = [device1_id]
        self.patch_and_check('{}/{}'.format(self.PACKAGES, package1_id), package1_patch)
        self.is_parent('package1', self.PACKAGES, device1_id, self.DEVICES)

        # Let's continue with
        #  Lot1
        #    |
        # Package1
        lot1 = self.get_fixture(self.LOTS, 'lot')
        lot1['label'] = 'lot1'
        lot1['children'] = {'packages': ['package1']}
        lot1_id = self.post_and_check(self.LOTS, lot1)['_id']
        # Let's check if the package is in the lot's children field and if the lot is in the ancestors' array
        # as a parent
        self.is_parent('lot1', self.LOTS, 'package1', self.PACKAGES)
        # and let's check if the lot is in the ancestor's array as a grandparent or above
        self.is_grandpa_or_above('lot1', self.LOTS, device1_id, self.DEVICES)

        # Let's continue with
        # Package1
        #    |
        # Package2
        package2 = self.get_fixture(self.PACKAGES, 'package')
        package2['label'] = 'package2'
        package2_id = self.post_and_check(self.PACKAGES, package2)['_id']
        package1_patch['children']['packages'] = ['package2']
        self.patch_and_check('{}/{}'.format(self.PACKAGES, package1_id), package1_patch)
        # This should be
        # Lot1
        #   |
        # Package1
        #   |    \______
        # Device1   Package2
        self.is_parent('package1', self.PACKAGES, 'package2', self.PACKAGES)
        self.is_grandpa_or_above('lot1', self.LOTS, device1_id, self.DEVICES)
        self.is_grandpa_or_above('lot1', self.LOTS, 'package2', self.PACKAGES)

        # Let's add place1 and place2
        place1 = self.get_fixture(self.PLACES, 'place')
        place1['label'] = 'place1'
        place1_id = self.post_and_check(self.PLACES, place1)['_id']
        place2 = self.get_fixture(self.PLACES, 'place')
        place2['label'] = 'place2'
        place2_id = self.post_and_check(self.PLACES, place2)['_id']
        # Let's make
        # Place1
        #   |
        # Place2
        place1_patch = {'@type': 'Place', 'children': {'places': ['place2']}}
        self.patch_and_check('{}/{}'.format(self.PLACES, place1_id), place1_patch)
        self.is_parent('place1', self.PLACES, 'place2', self.PLACES)

        # And now let's add place2-lot1 to have:
        # Place1
        #   |
        # Place2
        #   |
        # Lot1
        #   |
        # Package1
        #   |    \______
        # Device1   Package2
        place2_patch = {'@type': 'Place', 'children': {'lots': ['lot1']}}
        self.patch_and_check('{}/{}'.format(self.PLACES, place2_id), place2_patch)
        self.is_parent('place1', self.PLACES, 'place2', self.PLACES)
        self.is_parent('place2', self.PLACES, 'lot1', self.LOTS)
        self.is_parent('lot1', self.LOTS, 'package1', self.PACKAGES)
        self.is_parent('package1', self.PACKAGES, 'package2', self.PACKAGES)
        self.is_parent('package1', self.PACKAGES, device1_id, self.DEVICES)
        # But note how place1 and place 2 are not ancestors of package1, device1 and package2
        # as lots cannot inherit places to them, they need to set it manually.
        self.is_not_grandpa_or_above('place1', self.PLACES, device1_id, self.DEVICES)
        self.is_not_grandpa_or_above('place2', self.PLACES, device1_id, self.DEVICES)
        self.is_not_grandpa_or_above('place1', self.PLACES, 'package2', self.PACKAGES)
        self.is_grandpa_or_above('lot1', self.LOTS, device1_id, self.DEVICES)

        # We need to do the parenthood manually between place2 and package1
        # Device1 and package2 inherits everything from package1
        # Place1
        #   |
        # Place2
        #   |  |
        # Lot1 |
        #   |  |
        # Package1
        #   |    \______
        # Device1   Package2
        place2_patch['children']['packages'] = ['package1']
        self.patch_and_check('{}/{}'.format(self.PLACES, place2_id), place2_patch)
        self.is_parent('place2', self.PLACES, 'package1', self.PACKAGES)
        self.is_grandpa_or_above('place1', self.PLACES, device1_id, self.DEVICES)
        self.is_grandpa_or_above('place2', self.PLACES, device1_id, self.DEVICES)
        self.is_grandpa_or_above('place1', self.PLACES, 'package2', self.PACKAGES)

        # If we break the relationship between package1 and lot1, device1 and package2 should loose
        # relationship with lot1, place2, an place1
        lot1_patch = {'@type': 'Lot', 'children': {'packages': []}}
        self.patch_and_check('{}/{}'.format(self.LOTS, lot1_id), lot1_patch)
        self.is_not_parent('lot1', self.LOTS, 'package1', self.PACKAGES)
        self.is_not_grandpa_or_above('lot1', self.LOTS, device1_id, self.DEVICES)
        self.is_not_grandpa_or_above('lot1', self.LOTS, 'package2', self.PACKAGES)
        self.is_not_grandpa_or_above('place2', self.LOTS, device1_id, self.DEVICES)
        self.is_not_grandpa_or_above('place1', self.LOTS, 'package2', self.PACKAGES)

        # Let's add the relationship again
        lot1_patch = {'@type': 'Lot', 'children': {'packages': ['package1']}}
        self.patch_and_check('{}/{}'.format(self.LOTS, lot1_id), lot1_patch)
        self.is_parent('lot1', self.LOTS, 'package1', self.PACKAGES)
        self.is_grandpa_or_above('lot1', self.LOTS, device1_id, self.DEVICES)

        # Let's continue
        # Place1
        #   |
        #   |
        # Place2 Place3
        #   |  |    \
        # Lot1 |     \
        #   |  |      \
        # Package1     \
        #   |    \______\
        # Device1   Package2
        place3 = self.get_fixture(self.PLACES, 'place')
        place3['label'] = 'place3'
        place3['children'] = {'packages': ['package2']}
        place3_id = self.post_and_check(self.PLACES, place3)['_id']
        self.is_parent('place3', self.PLACES, 'package2', self.PACKAGES)

        # Place1
        #   |  \
        #   |   \__
        # Place2 Place3
        #   | |     \
        # Lot1|      \
        #   | |       \
        # Package1     \
        #   |    \______\
        # Device1   Package2
        place1_patch['children']['places'].append('place3')
        self.patch_and_check('{}/{}'.format(self.PLACES, place1_id), place1_patch)
        self.is_parent('place1', self.PLACES, 'place3', self.PLACES)
        self.is_grandpa_or_above('place1', self.PLACES, 'package2', self.PACKAGES)

        # Now if I cut package2 - Package1, place1 will still be ancestor of package2
        package1_patch['children']['packages'].remove('package2')
        self.patch_and_check('{}/{}'.format(self.PACKAGES, package1_id), package1_patch)
        self.is_not_parent('package1', self.PACKAGES, 'package2', self.PACKAGES)
        self.is_grandpa_or_above('place1', self.PLACES, 'package2', self.PACKAGES)

        # Let's redo package1-package2
        package1_patch['children']['packages'].append('package2')
        self.patch_and_check('{}/{}'.format(self.PACKAGES, package1_id), package1_patch)
        self.is_parent('package1', self.PACKAGES, 'package2', self.PACKAGES)

        # Place1
        #   |  \
        #   |   \__
        # Place2 Place3
        #   |       \
        # Lot1       \
        #   |         \
        # Package1     \
        #   |    \______\
        # Device1   Package2
        #              |
        #           Device2
        package2_patch = {'@type': 'Package', 'children': {'devices': [device2_id]}}
        self.patch_and_check('{}/{}'.format(self.PACKAGES, package2_id), package2_patch)
        self.is_parent('package2', self.PACKAGES, device2_id, self.DEVICES)
        self.is_grandpa_or_above('place3', self.PLACES, device2_id, self.DEVICES)

        # Place1
        #   |  \
        #   |   \__
        # Place2 Place3
        # | |  __/
        # |Lot1______
        # | |        \
        # Package1    \
        #   |    \___  \
        # Device1   Package2
        #              |
        #           Device2
        # Let's remove package2 - place3 and add place3 - lot1
        # Note that this is going to make
        place3_patch = {'@type': 'Place', 'children': {'packages': [], 'lots': ['lot1']}}
        self.patch_and_check('{}/{}'.format(self.PLACES, place3_id), place3_patch)
        self.is_not_parent('place3', self.PLACES, 'package2', self.PACKAGES)
        self.is_not_grandpa_or_above('place3', self.PLACES, device2_id, self.DEVICES)
        self.is_parent('place3', self.PLACES, 'lot1', self.LOTS)
        # Add lot1 - package2
        lot1_patch['children']['packages'].append('package2')
        self.patch_and_check('{}/{}'.format(self.LOTS, lot1_id), lot1_patch)
        self.is_parent('lot1', self.LOTS, 'package2', self.PACKAGES)
        # Note how place3 is not still an ancestor of package2 as it comes through a lot it needs to be
        # set specifically
        self.is_not_grandpa_or_above('place3', self.PLACES, device2_id, self.DEVICES)
        # ...and of device1
        self.is_not_grandpa_or_above('place3', self.PLACES, 'package1', self.PACKAGES)
        self.is_not_grandpa_or_above('place3', self.PLACES, device1_id, self.DEVICES)
        # But place1 it is, as ti goes through place2 and package1
        self.is_grandpa_or_above('place1', self.PLACES, 'package2', self.PACKAGES)
        self.is_grandpa_or_above('place1', self.PLACES, device2_id, self.DEVICES)

        # Place1
        #   |  \
        #   |   \__
        # Place2 Place3          Lot5
        # | |_____/               /
        # |Lot1_______           Lot3
        # | |        \
        # Package1    \
        #   |    \___  \
        # Device1   Package2
        #              |
        #           Device2
        lot3 = self.get_fixture(self.LOTS, 'lot')
        lot3['label'] = 'lot3'
        lot3_id = self.post_and_check(self.LOTS, lot3)['_id']
        lot5 = self.get_fixture(self.LOTS, 'lot')
        lot5['label'] = 'lot5'
        lot5['children'] = {'lots': ['lot3']}
        lot5_id = self.post_and_check(self.LOTS, lot5)['_id']
        self.is_parent('lot5', self.LOTS, 'lot3', self.LOTS)

        # Place1
        #   |  \
        #   |   \__
        # Place2 Place3          Lot5
        # | |_____/               /
        # |Lot1_______           Lot3
        # | |        \
        # Package1    \
        #   |    \___  \
        # Device1   Package2
        #              |    \_____
        #           Device2    Device3
        package2_patch['children']['devices'].append(device3_id)
        self.patch_and_check('{}/{}'.format(self.PACKAGES, package2_id), package2_patch)
        self.is_parent('package2', self.PACKAGES, device3_id, self.DEVICES)
        self.is_not_grandpa_or_above('place3', self.PLACES, device3_id, self.DEVICES)

        # Place1
        #   |  \
        #   |   \__
        # Place2 Place3          Lot5
        # |  |_____/               /
        # |Lot1_______           Lot3
        # |  |        \           |
        # Package1    \          |
        #   |    \___  \         |
        # Device1   Package2   Package3
        #              |    \_____
        #           Device2    Device3
        package3 = self.get_fixture(self.PACKAGES, 'package')
        package3['label'] = 'package3'
        package3_id = self.post_and_check(self.PACKAGES, package3)['_id']
        lot3_patch = {'@type': 'Lot', 'children': {'packages': ['package3']}}
        self.patch_and_check('{}/{}'.format(self.LOTS, lot3_id), lot3_patch)
        self.is_parent('lot3', self.LOTS, 'package3', self.PACKAGES)

        # Place1
        #   |  \
        #   |   \__
        # Place2 Place3      Lot4 Lot5
        # |  |_____/               /
        # |Lot1_______           Lot3
        # |  |        \           |
        # Package1    \          |
        #   |    \___  \         |
        # Device1   Package2   Package3
        #              |         |
        #           Device2    Device3
        # As a device can only have one package, once we set it to package3 it will loose package2
        package3_patch = {'@type': 'Package', 'children': {'devices': [device3_id]}}
        self.patch_and_check('{}/{}'.format(self.PACKAGES, package3_id), package3_patch)
        self.is_parent('package3', self.PACKAGES, device3_id, self.DEVICES)
        self.is_not_parent('package2', self.PACKAGES, device3_id, self.DEVICES)
        not_ancestors = (('lot1', self.LOTS), ('place2', self.PLACES), ('place3', self.PLACES), ('place1', self.PLACES))
        for name, resource_name in not_ancestors:
            self.is_not_grandpa_or_above(name, resource_name, device3_id, self.DEVICES)
        self.is_grandpa_or_above('lot3', self.LOTS, device3_id, self.DEVICES)
        self.is_grandpa_or_above('lot5', self.LOTS, device3_id, self.DEVICES)

        # Place1
        #   |  \
        #   |   \__
        # Place2 Place3      Lot4 Lot5
        # |  |_____/             \  /
        # |Lot1_______           Lot3
        # |  |        \           |
        # Package1    \          |
        #   |    \___  \         |
        # Device1   Package2   Package3
        #              |         |
        #           Device2    Device3
        lot4 = self.get_fixture(self.LOTS, 'lot')
        lot4['label'] = 'lot4'
        lot4['children'] = {'lots': ['lot3']}
        lot4_id = self.post_and_check(self.LOTS, lot4)['_id']
        self.is_parent('lot4', self.LOTS, 'lot3', self.LOTS)
        self.is_grandpa_or_above('lot4', self.LOTS, 'package3', self.PACKAGES)
        self.is_grandpa_or_above('lot4', self.LOTS, device3_id, self.DEVICES)

        # todo we need to ensure the ui explains this: if you change the place of a device in a package
        # you automatically move it out from the package
        # Place1
        #   |  \
        #   |   \__
        # Place2 Place3      Lot4 Lot5
        #   |_____/   \         \  /
        # Lot1_______  \        Lot3
        #   |        \  \        |
        # Package1    \  \__     |
        #   |    \___  \    \    |
        # Device1   Package2 \ Package3
        #              |      \  |
        #           Device2    Device3
        place3_patch['children']['devices'] = [device3_id]
        self.patch_and_check('{}/{}'.format(self.PLACES, place3_id), place3_patch)
        self.is_parent('place3', self.PLACES, device3_id, self.DEVICES)
        self.is_not_parent('package2', self.PACKAGES, device3_id, self.DEVICES)
        self.is_not_grandpa_or_above('lot3', self.LOTS, device3_id, self.DEVICES)
        self.is_grandpa_or_above('place1', self.PLACES, device3_id, self.DEVICES)
        # Let's remove it
        place3_patch['children']['devices'] = []
        self.patch_and_check('{}/{}'.format(self.PLACES, place3_id), place3_patch)
        self.is_not_parent('place3', self.PLACES, device3_id, self.DEVICES)

        # But this yes
        # Place1
        #   |  \
        #   |   \__
        # Place2 Place3      Lot4 Lot5
        #   |_____/   \         \  /
        # Lot1_______  \        Lot3
        #   |        \  \        |
        # Package1    \  \_____  |
        #   |    \___  \       \ |
        # Device1   Package2   Package3
        #              |         |
        #           Device2    Device3
        place3_patch['children']['packages'] = ['package3']
        self.patch_and_check('{}/{}'.format(self.PLACES, place3_id), place3_patch)
        self.is_parent('place3', self.PLACES, 'package3', self.PACKAGES)
        self.is_grandpa_or_above('place3', self.PLACES, device3_id, self.DEVICES)

        # A device can be in two lots easily
        # Place1
        #   |  \
        #   |   \__
        # Place2 Place3      Lot4 Lot5__
        #   |_____/   \         \  /    \
        # Lot1_______  \        Lot3 ___ \
        #   |        \  \        |      \|
        # Package1    \  \_____  |       \
        #   |    \___  \       \ |        \
        # Device1   Package2   Package3    \
        #              |         |         |
        #           Device2    Device3  Device4
        lot3_patch['children']['devices'] = [device4_id]
        self.patch_and_check('{}/{}'.format(self.LOTS, lot3_id), lot3_patch)
        self.is_parent('lot3', self.LOTS, device4_id, self.DEVICES)
        self.is_grandpa_or_above('lot5', self.LOTS, device4_id, self.DEVICES)  # Lot 5 is already a grandparent or above
        self.is_grandpa_or_above('lot4', self.LOTS, device4_id, self.DEVICES)
        lot5_patch = {'@type': 'Lot', 'children': {'devices': [device4_id], 'lots': ['lot3']}}
        self.patch_and_check('{}/{}'.format(self.LOTS, lot5_id), lot5_patch)
        self.is_parent('lot5', self.LOTS, device4_id, self.DEVICES)  # Lot 5 is parent
        self.is_grandpa_or_above('lot5', self.LOTS, device4_id, self.DEVICES)  # And keeps being a grandparent/above
        self.is_grandpa_or_above('lot4', self.LOTS, device4_id, self.DEVICES)

        # let's add device4 to a new place
        # Place1
        #   |  \
        #   |   \__
        # Place2 Place3      Lot4 Lot5__
        #   |_____/   \         \  /    \
        # Lot1_______  \        Lot3 ___ \
        #   |        \  \        |      \|
        # Package1    \  \_____  |       \
        #   |    \___  \       \ |        \ Place4
        # Device1   Package2   Package3    \/
        #              |         |         |
        #           Device2    Device3  Device4
        place4 = self.get_fixture(self.PLACES, 'place')
        place4['label'] = 'place4'
        place4['children'] = {'devices': [device4_id]}
        place4_id = self.post_and_check(self.PLACES, place4)['_id']
        self.is_parent('place4', self.PLACES, device4_id, self.DEVICES)
        # The rest is the same for device4
        self.is_parent('lot5', self.LOTS, device4_id, self.DEVICES)
        self.is_grandpa_or_above('lot5', self.LOTS, device4_id, self.DEVICES)
        self.is_grandpa_or_above('lot4', self.LOTS, device4_id, self.DEVICES)

        # If we add a place to lot5/lot3/lot4
        # The actual place of device4 is still place4 as
        # resources do not inherit places from lots; they need to be specifically set
        # Place1 _________________
        #   |  \                  \
        #   |   \__                \
        # Place2 Place3      Lot4 Lot5__
        #   |_____/   \         \  /    \
        # Lot1_______  \        Lot3 ___ \
        #   |        \  \        |      \|
        # Package1    \  \_____  |       \
        #   |    \___  \       \ |        \ Place4
        # Device1   Package2   Package3    \/
        #              |         |         |
        #           Device2    Device3  Device4
        place1_patch['children']['lots'] = ['lot5']
        self.patch_and_check('{}/{}'.format(self.PLACES, place1_id), place1_patch)
        self.is_parent('place1', self.PLACES, 'lot5', self.LOTS)
        self.is_not_grandpa_or_above('place1', self.PLACES, device4_id, self.DEVICES)
        # But note that device3 it still has place1 as an ancestor
        # because it gets it from package3 - place3 - place1
        # devices inherit everything from packages, they are quite tied together
        self.is_grandpa_or_above('place1', self.PLACES, device3_id, self.DEVICES)

        # Do we want to device4 to be in the same place as its lots?
        # Let's make place1 parent direct from device4
        # Place1 _________________
        #   |  \                  \____
        #   |   \__                \   \
        # Place2 Place3      Lot4 Lot5__|
        #   |_____/   \         \  /    \
        # Lot1_______  \        Lot3 ___ \
        #   |        \  \        |      \|
        # Package1    \  \_____  |       \
        #   |    \___  \       \ |        \ Place4
        # Device1   Package2   Package3    \
        #              |         |         |
        #           Device2    Device3  Device4
        # Note that this deletes the relationship with place4; a device can only be in one place at a time
        # (unless this place is inside another place, and this is the inheritance)
        place1_patch['children']['devices'] = [device4_id]
        self.patch_and_check('{}/{}'.format(self.PLACES, place1_id), place1_patch)
        self.is_parent('place1', self.PLACES, device4_id, self.DEVICES)
        self.is_not_parent('place4', self.PLACES, device4_id, self.DEVICES)

    def test_prohibited_actions(self):
        # Add a place in a lot
        lot = self.get_fixture(self.LOTS, 'lot')
        label_lot = lot['label']
        lot_id = self.post_and_check(self.LOTS, lot)['_id']
        place = self.get_fixture(self.PLACES, 'place')
        place['label'] = place_label = 'place1'
        self.post_and_check(self.PLACES, place)['_id']
        lot_patch = {'@type': 'Lot', 'children': {'places': [place_label]}}
        _, status = self.patch('{}/{}'.format(self.LOTS, lot_id), lot_patch)
        self.assert422(status)
        self.is_not_parent(place_label, self.PLACES, label_lot, self.LOTS)

        # todo test more...
