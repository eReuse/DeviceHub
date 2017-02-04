"""
We mimic https://schema.org/unitCode, in concrete
the UN/CEFACT Common Code.
"""
from ereuse_devicehub.resource_proxy import ResourceProxy
from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.resource import Resource
from ereuse_devicehub.utils import Naming, NestedLookup, ClassProperty


class UnitCodes:
    mbyte = '4L'
    mbps = 'E20'
    mhz = 'MHZ'
    gbyte = 'E34'
    ghz = 'A86'
    bit = 'A99'
    kgm = 'KGM'
    m = 'MTR'

    @classmethod
    def humanize(cls, code_to_search):
        for human_name, code in vars(cls).items():
            if code == code_to_search:
                return human_name


class Schema(Resource):
    """
    Schemas configure the fields of a resource.
    """

    prefix = None
    """The prefix of the class. Modify it and the class and its descendants will inherit it nicely"""

    def generate_config(self) -> dict:
        """
        Generates the config dictionary of the schema. This is, the ancestor's fields + our fields + the
        descendant's fields,
        """
        fields = super(Schema, self).generate_config()  # We get the fields of our ancestors and ours
        for descendant in self.descendants:  # We get the fields of our descendants
            descendant_fields = descendant.actual_fields()
            fields.update(descendant_fields)
            # Our resource (ex. Device) has to allow sub-resources (ex. ComputerMonitor, HardDrive)
            if '@type' in fields:
                fields['@type']['allowed'] |= descendant_fields.get('@type', {}).get('allowed', set())
            if 'type' in fields:
                fields['type']['allowed'] |= set(descendant_fields.get('type', {}).get('allowed', set()))
        # Let's execute any callable (like fields with references)
        references = []
        NestedLookup(fields, references, callable)
        for document, ref_key in references:
            document[ref_key] = document[ref_key]()
        return fields

    # noinspection PyNestedDecorators
    @ClassProperty
    @classmethod
    def type(cls):
        """Get the type of the resource. Note how this is a classmethod and you can use it nicely."""
        return Naming.new_type(cls.__name__, prefix=cls.prefix)

    # noinspection PyNestedDecorators
    @ClassProperty
    @classmethod
    def resource(cls):
        """As type() but for the resource name."""
        return Naming.resource(cls.type)

    @property
    def types(self):
        """Get the types of the actual class and all the descendants"""
        yield self.type
        for descendant in self.descendants:
            yield descendant.type

    @property
    def resource_types(self):
        for _type in self.types:
            yield Naming.resource(_type)


class RDFS(Schema):
    # todo import_schemas and abstract fields?
    def __init__(self, proxy: ResourceProxy, **kwargs):
        # Let's create a default personalized @type for everyone. User can override it in self.config()
        # as @type is set before config is called
        setattr(self, '@type', {
            'type': 'string',
            'required': True,
            'teaser': False,
            'allowed': [self.type]
        })
        super().__init__(proxy, **kwargs)

    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.label = {
            'type': 'string',
            'sink': 5,
            'description': 'A short, descriptive title'
        }
        self.created = {
            'type': 'datetime',
            'dh_allowed_write_roles': Role.SUPERUSER,
            'writeonly': True,
            'doc': 'Sets the _created and _updated, thought to be used in imports.'
        }


class Thing(RDFS):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.url = {
            'type': 'url',
            'teaser': False,
            'doc': 'The url of the resource. If passed in, the value it is moved to sameAs.',
            'move': 'sameAs'
        }
        self.sameAs = {
            'type': 'list',
            'teaser': False,
            # 'readonly': True, todo should be readonly
            'unique': True,
        }
        self.description = {
            'type': 'string',
            'maxlength': 500,
            'sink': -4,
            'description': 'Full long description'
        }
