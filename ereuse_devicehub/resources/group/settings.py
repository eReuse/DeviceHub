import copy

import pymongo

from ereuse_devicehub.resources.resource import ResourceSettings
from ereuse_devicehub.resources.schema import Thing

ancestors = {
    'type': 'list',
    'schema': {
        '@type': {
            'type': 'string'
        },
        'label': {
            'type': 'string',
            'doc': 'Although this is a data relation, we cannot specify it to eve as datasources'
                   'are different. This is an ordered set of values where the first is the parent.'
        }
    },
    'materialized': True
}

place_fk = {
    'type': 'string',
    'data_relation': {
        'resource': 'places',
        'embeddable': True,
        'field': 'label'
    }
}
places_fk = {
    'type': 'list',
    'schema': place_fk,
    'unique_values': True
}

package_fk = {
    'type': 'string',
    'data_relation': {
        'resource': 'packages',
        'embeddable': True,
        'field': 'label'
    }
}
packages_fk = {
    'type': 'list',
    'schema': package_fk,
    'unique_values': True
}

lot_fk = {
    'type': 'string',
    'data_relation': {
        'resource': 'lots',
        'embeddable': True,
        'field': 'label'
    }
}
lots_fk = {
    'type': 'list',
    'schema': lot_fk,
    'unique_values': True
}

lots_lots_fk = {
    'type': 'list',
    'schema': {
        'type': 'list',
        'schema': lot_fk
    }
}

devices_fk = {
    'type': 'list',
    'schema': {
        'type': 'string',
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        }
    },
    'unique_values': True
}

children_groups = {
    'type': 'list',
    'schema': {
        'type': 'string'
    },
    'doc': 'This is a data-relation but eve disallows it for multiple resources (lot, package...)'
}


class Group(Thing):
    """
    Groups 'group' devices in different ways. Some of them represent physical groupings like a place or a package,
    and others are abstract, like a lot. Physical groupings let you locate and find your devices in the real-world
    easily, and abstract ones serve you to organize the devices better –you can view and work with devices selecting
    only the group, for example, performing an event on the group is performed to all of its devices.
    Finally, groups are hierarchical, so you can have them inside others, but there are rules.

    Restrictions in groups
    ======================

    - Moving devices
      - If you move a package from another group you do it so for its devices. If you want to move a device in a different
         place than its package, remove it first from the package.
      - Given an abstract group with a place set, if you add a device this is not automatically set to the place. You can know
         for a given group which devices are not in the same place, and you can set all of them to that place.
      - Given an abstract group with devices, if you change the place of the abstract group, it will not change for its devices.
    - Nesting
      - Places and lots can only have one parent.
      - Packages and devices can have multiple lots as parents, but only one phyisical (place).
        The last set lot is the actual parent.
      - Devices and packages can have only one package as a parent.

    The relationships
    =================
    The rules of the hierarchy are as follows:

    Each type of group occupies a level of the hierarchy. Places are on the top level, lots come after, then
    packages and, finally although not a group, devices. As relationships are bottom-up, places can
    only be children of parents, lots can be children of lots and places, packages can be children of packages,
    lots and places; and finally devices can be children of places, lots and packages.

    A group can only have one parent, except packages, like with devices, can have multiple *lots*, they still can
    only have one package or place as a parent.

    Given a lot L1 child of a place PL1, a package PK1 child of a place PL2 and a device D1, we set as L1 and
    PK1 as the parents of D1.

    - The parents are L1, PK1.
    - The ancestors are L1, Pk1, and PL1 or PL2? A device can only be in one place. Conflict resolution: we take
      the place of the last assignment, which is PK1, so the ancestors are L1, Pk1 and PL2.
    This is seen as:
    - device.ancestors.place.PL2 = []  # As is the place we want to do
    - device.ancestors.lots = [L1] # If L1 were inside other lots, we would show them here. If the device had L1 and a new
      L3 as parents, and L3 would be L4, the device.ancestors.lots = [L1, L3, L4] Note this is unordered.
      device.ancestors
    - device.ancestors.packages = [PK1]
    - device.parents.place = Pl2
    - device.parents.lots = [L1]
    - device.parents.package = PK1

    We want this to answer "is device/group a descendant of X?", "is device/group the child of X?", "is this a top
    node" (device.parents.place/lots/package is empty)

    The fields:
    Note that 'ancestors' is materialized and that only ancestors.lots is going to have more than two elements in
    the dict, as lots are the only ones having more than one parent.
    - Place
      - ancestors: {'places': {parentName: []}}
      - children: {'places': [], 'lots': [], 'packages': [], 'devices': []}
    - Lot
      - ancestors: {'place': {parentName: []}, 'lots': {parentName: [], parentName1: []}}
      - children: {'lots': [], 'packages': [], 'devices': []}
    - Package
      - ancestors: {'place': {parentName: []}, {'lots': {parentName: []}}, {'packages': {parentName: []}}}
      - children: {'packages': [], 'devices': []}
    - Device
      - ancestors: {'place': {parentName: []}, {'lots': {parentName: []}}, {'packages': {parentName: []}}}


    - parents: {'places': ''}
    - parents: {'places': '', 'lots': []}
    - parents: {'place': '', 'lots': [], 'package': ''}
    - parents: {'place': '', 'lots': [], 'package': ''}


    Is X, a device or a package, descendant of Y, a place? Resolution:
      1. If X has Y as parent, return True.
      2. If X has a place, return true if any of its ancestors is Y.
      3. If X has a package as parent, return true any of its ancestors is Y.

    Is X, a device, descendant of Y, a lot? Resolution:
      1. return true if X has Y as parent.
      2. if X has lots, return true if any of their ancestors is Y.







    Given Y of type A. Is X of type

    look from the lower hierarchy elment i
    - If X is Place: search only from the actual place ancestors
    - If X is Lot: search from all lots

    An example showing all the kinds of relationships
    -------------------------------------------------

            Place1          Place4
              |               |
            /   \           Lot4 Lot5
        Place2  Place3        \  /
          | \      | \         \/
       Lot1 Lot2   |  \      Lot3
        | \_______ |   \      /|
        |         \|   |    /  |
    Package1  Package2 |  /    |
       |  \____        | /     |
       |       \       |/      |
       |    Package3   |       |
       |        |      |       |
    Device1 Device2 Device3  Device4

    How to work with groups
    =======================

    You POST / PATCH / PUT relationships through Group's children attribute, and then the other attributes
    are materialized.
    """
    byUser = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True
        },
        'readonly': True
    }
    label = copy.deepcopy(Thing.label)
    label['required'] = True
    label['unique'] = True


class GroupSettings(ResourceSettings):
    resource_methods = ['GET', 'POST']
    item_methods = ['GET', 'PATCH', 'DELETE', 'PUT']
    _schema = Group
    datasource = {
        'default_sort': [('_created', -1)],
        'source': 'groups'
    }
    extra_response_fields = ResourceSettings.extra_response_fields + ['children', 'ancestors', 'byUser', 'devices']
    mongo_indexes = {
        '@type and label': [('@type', pymongo.DESCENDING), ('label', pymongo.DESCENDING)],
    }
