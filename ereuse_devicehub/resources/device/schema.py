from ..schema import UnitCodes, Thing


class Product(Thing):
    model = {
        'type': 'string',
        'sink': 4
    }
    weight = {
        'type': 'float',
        'unitCode': UnitCodes.kgm,
        'sink': -1,
        'teaser': False
    }
    width = {
        'type': 'float',
        'unitCode': UnitCodes.m,
        'sink': -1,
        'teaser': False
    }
    height = {
        'type': 'float',
        'unitCode': UnitCodes.m,
        'sink': -1,
        'teaser': False
    }
    manufacturer = {
        'type': 'string',
        'sink': 4
    }
    productId = {
        'type': 'string',
        'sink': 3,
        'teaser': False
    }


class IndividualProduct(Product):
    serialNumber = {
        'type': 'string',
        'sink': 4
    }


class Device(IndividualProduct):
    """Class Device"""
    _id = {
        'type': 'string',
        'unique': True,
        'device_id': True,
        'sink': 4,
        'teaser': False
        # ALLOWED_WRITE_ROLES: Role.SUPERUSER  # For recovery purposes
    }
    icon = {
        'type': 'string',
        'readonly': True,
        'teaser': False,
        'sink': -5
    }
    hid = {
        'type': 'hid',
        'sink': 5,
        'teaser': False
    }
    pid = {
        'type': 'string',
        'unique': True,
        'sink': 5
    }
    isUidSecured = {
        'type': 'boolean',
        'default': True,
        'teaser': False
    }
    labelId = {
        'type': 'string',  # Materialized label of the last snapshot
        'sink': 5
    }
    components = {
        'type': 'list',
        'schema': {
            'type': 'string',
            'data_relation': {
                'resource': 'devices',
                'embeddable': True,
                'field': '_id'
            }
        },
        'sink': 1,
        'default': []
    }
    place = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'places',
            'embeddable': True,
            'field': '_id'
        },
        'readonly': True,  # Materialized
        'sink': 2
    }
    owners = {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'accounts',
                'embeddable': True,
                'field': '_id'
            }
        },
        'readonly': True,  # Materialized
        'sink': 2
    }
    public = {
        'type': 'boolean',
        'default': False
    }
