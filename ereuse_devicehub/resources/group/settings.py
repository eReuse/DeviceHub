import copy

import pymongo

from ereuse_devicehub.resources import events_pk_schema
from ereuse_devicehub.resources.resource import ResourceSettings
from ereuse_devicehub.resources.schema import Thing


class Group(Thing):
    """
    Groups 'group' devices in different ways. Some of them represent physical groupings like a place or a package,
    and others are abstract, like a lot. Physical groupings let you locate and find your devices in the real-world
    easily, and abstract ones serve you to organize the devices better –you can view and work with devices selecting
    only the group, for example, performing an event on the group is performed to all of its devices.
    Finally, groups are hierarchical, so you can have them inside others, but there are rules.

    Each type of group occupies a level of the hierarchy. Places are on the top level, lots come after, then
    packages and, finally although not a group, devices. As relationships are bottom-up: places can
    only be children of other places, lots can be children of lots and places, packages can be children of packages,
    lots and places; and finally devices can be children of places, lots and packages.

    Places, devices and packages can only have one parent. As physical resources, they can only be in one physical
    space in a given time. Note that you can have a device inside a package, that is inside another package, that is
    inside a place. They only have one parent, but tey have many ancestors. On the other side, as lots are
    abstract they can have multiple parents.

    Packages and lots are strongly united, if you *move* a lot in a place, you move its devices. This is not true for
    lots: if you set a lot in a place its devices and packages are not set to the place, you need to manually do so.
    This is to let you set a place for a lot in a given time, and let an employee in the warehouse physically
    move the devices in a later time. You can get which devices of a given lot are not in the place where the lot is.

    How to work with groups
    =======================
    You POST / PATCH / PUT relationships through Group's children attribute, and then the other attributes
    are materialized. The children's attribute is: group.children: {'typeofChildren': [labels or ids]}
    Labels for groups and _id for devices.
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
    children = {
        'type': 'dict',
        'schema': {},  # Let make each group type define it
        'default': {}
    }
    ancestors = {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                '@type': {
                    'type': 'string',
                    'allowed': {'Lot', 'IncomingLot', 'OutgoingLot', 'Place', 'Package'}
                },
                'label': {
                    'type': 'string',
                    'doc': 'Although this is a data relation, we cannot specify it to eve as datasources'
                           'are different. This is an ordered set of values where the first is the parent.'
                }
            }
        },
        'default': [],
        'materialized': True
    }
    events = events_pk_schema.events


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
        'Group: updated': [('_updated', pymongo.DESCENDING)],
        'Group: updated, label': [('label', pymongo.TEXT), ('_updated', pymongo.DESCENDING)],
    }
    additional_lookup = {
        'url': r'regex("([\w]).+")',
        'field': 'label',
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

pallet_fk = {
    'type': 'string',
    'data_relation': {
        'resource': 'pallets',
        'embeddable': True,
        'field': 'label'
    }
}

pallets_fk = {
    'type': 'list',
    'schema': pallet_fk,
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
