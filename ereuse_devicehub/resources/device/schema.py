from ..schema import UnitCodes, Thing


class Product(Thing):
    model = {
        'type': 'string',
        'sink': 4,
        'short': 'Mod.',
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
        'sink': 4,
        'short': 'Man.'
    }
    productId = {
        'type': 'string',
        'sink': 3,
        'teaser': False
    }


class IndividualProduct(Product):
    serialNumber = {
        'type': 'string',
        'sink': 4,
        'short': 'S/N'
    }


class Device(IndividualProduct):
    """Class Device"""
    _id = {
        'type': 'string',
        'unique': True,
        'device_id': True,
        'sink': 4,
        'teaser': False,
        'short': 'ID',
        'description': 'The System ID, or simply ID, is an easy-to-read internal id.',
        'uid': True
        # ALLOWED_WRITE_ROLES: Role.SUPERUSER  # For recovery purposes
    }
    hid = {
        'type': 'hid',
        'sink': 5,
        'teaser': False,
        'short': 'HID',
        'description': 'The Hardware ID is the unique ID traceability systems use to ID a device globally.',
        'doc': 'The unique constrained is evaluated manually as this field needs to be computed',
        'uid': True
    }
    pid = {
        'type': 'string',
        'unique': True,
        'sink': 5,
        'short': 'Platform ID',
        'description': 'The PID identifies a device under a circuit or platform.',
        'uid': True,
        'externalSynthetic': True
    }
    rid = {
        'type': 'string',
        'unique': True,
        'short': 'Receiver ID',
        'description': 'The Receiver ID is the internal identifier a Refurbisher uses.',
        'uid': True,
        'externalSynthetic': True
    }
    gid = {
        'type': 'string',
        'unique': True,
        'short': 'Giver ID',
        'description': 'The Giver ID links the device to the giver\'s (donor, seller) internal inventory.',
        'uid': True,
        'externalSynthetic': True
    }
    isUidSecured = {
        'type': 'boolean',
        'default': True,
        'teaser': False
    }
    labelId = {
        'type': 'string',  # Materialized label of the last snapshot
        'sink': 5,
        'short': 'Label'
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
        'materialized': True,
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
        'materialized': True,
        'sink': 2
    }
    public = {
        'type': 'boolean',
        'default': False
    }
    events = {
        'type': 'list',
        'schema': {
            'type': 'dict'
        },
        'materialized': True
    }
    placeholder = {
        'type': 'boolean',
        'default': False,
        'doc': 'Invalid for components.'
    }

    @classmethod
    def subclasses_fields(cls):
        """We remove the 'required' clause from the aggregation"""
        fields = super().subclasses_fields()
        if cls == Device:
            del fields['model']['required']
            del fields['serialNumber']['required']
            del fields['manufacturer']['required']
            del fields['type']['required']
        return fields
