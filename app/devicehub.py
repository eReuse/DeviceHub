import copy
from importlib import import_module

import inflection
from eve import Eve
from eve.flaskapp import RegexConverter
from eve.io.mongo import Mongo, GridFSMediaStorage, Validator
from eve.logging import RequestFilter

from app.utils import Naming


class DeviceHub(Eve):
    def __init__(self, import_name=__package__, settings='settings.py', validator=Validator, data=Mongo, auth=None,
                 redis=None, url_converters=None, json_encoder=None, media=GridFSMediaStorage, **kwargs):
        """
            It exactly does the same as Eve's __init__ (copy & paste). It just changes one line:
            self.register_resource(resource, settings)
                    to
            self.register_resource(resource, self.config['DOMAIN'][resource])
            Otherwise we loose references between schemas, not updating accordingly when registering
        """
        super(Eve, self).__init__(import_name, **kwargs)

        # add support for request metadata to the log record
        self.logger.addFilter(RequestFilter())

        self.validator = validator
        self.settings = settings

        self.load_config()
        self.validate_domain_struct()

        # enable regex routing
        self.url_map.converters['regex'] = RegexConverter

        # optional url_converters and json encoder
        if url_converters:
            self.url_map.converters.update(url_converters)

        self.data = data(self)
        if json_encoder:
            self.data.json_encoder_class = json_encoder

        self.media = media(self) if media else None
        self.redis = redis

        if auth:
            self.auth = auth() if callable(auth) else auth
        else:
            self.auth = None

        self._init_url_rules()
        self._init_media_endpoint()
        self._init_schema_endpoint()

        if self.config['OPLOG'] is True:
            self._init_oplog()

        # validate and set defaults for each resource

        # Use a snapshot of the DOMAIN setup for iteration so
        # further insertion of versioned resources do not
        # cause a RuntimeError due to the change of size of
        # the dict
        domain_copy = copy.deepcopy(self.config['DOMAIN'])
        for resource, settings in domain_copy.items():
            self.register_resource(resource, self.config['DOMAIN'][resource])

        # it seems like both domain_copy and config['DOMAIN']
        # suffered changes at this point, so merge them
        # self.config['DOMAIN'].update(domain_copy)

        self.register_error_handlers()

    def register_resource(self, resource, settings, superclasses=None):
        """
            Recursively registers a resource and it's sub-resources.

            Recursive registering imitates the extension (heriarchy) of classes. You can extend resources by adding
            more specialized sub-resources. This is the case of 'Event' and 'TestHardDrive', 'TestHardDrive' is extending
            'Event' because:
            - It inherits all the properties of device (which can override)
            - They share the same database collection
            - It's URL is under Event: 'events/test-hard-drive'
            Extension is as deep as you want. For example a 'GraphicCard' extends from 'Component', which extends from
            'Device'.

            This is the process:
            1. Register the resource. If this has a super-resource, register the super-resource first.
            2. If the resource has some fields in its settings, it will automatically trigger the recursive registering.
            3. For every sub-resource, it will recursively look for sub-resources.
            4. The sub-resource will update the super-resource. The super-resource
            will contain all values from all their sub-resources, recursively. This is, because if we want to access
            'events' for example, we want to retrieve all properties of all sub-resources, not just the ones defined
            in 'events'. This is different from extending classes, as the super-class is not supposed to contain
            all properties and methods of their sub-classes.

            These are the properties you can set to a super-resource to automatically register its sub-resources:
            Add a dict 'is_super_class_of' in the settings param of the super-resource. This dict can have 2 attributes:
            - An attribute called 'modules' that contains a list of PascalTyped sub-resources
            which settings files need to be loaded from a submodule where the super-class module is.
            This is the way device and event works
            - An attribute called 'generic' that contains a list of PascalTyped sub-resources that
            are generic, which means their structure is the same for them. This structure must exist
            as a dictionary in the passed-in settings named 'generic_schema'

            In the 4th step, it can happen that 2 sub-resources set the same property name but have different meanings
            (for example, the test field of a HardDrive is different from the test field of a Processor). In this case,
            you can use a hook, that is executed after registering all the sub-resources, so you can update the schema
            of your super-resource accordingly. Add a property to your settings param named 'merge_hook' that contains
            a method. We pass the following parameters to the method: 1. the app object, 2. the reosource name, 3.
            the settings file, 4. an ordered list of superclasses, if any. You are supposed to invoke update_resource from
            this class to update the resource.
        """
        superclasses = [] if superclasses is None else superclasses
        super().register_resource(resource, settings)  # We register the actual resource
        superclasses.append(Naming.python(resource))  # And we added as a superclass for the sub-resources
        super_class_of = settings.get('is_super_class_of', {})
        for sub_resource in super_class_of.get('modules', []):
            type_u = Naming.python(sub_resource)
            sub_resource_settings = import_module('{}.{}.{}.settings'.format('app', '.'.join(superclasses), type_u))
            self.register_subresource(sub_resource, getattr(sub_resource_settings, type_u + '_settings'), superclasses)
        for sub_resource in super_class_of.get('generic', []):
            self.register_subresource(sub_resource, copy.deepcopy(settings['generic_schema']), superclasses)
        if 'merge_hook' in settings:
            settings['merge_hook'](self, resource, settings, superclasses)

    def register_subresource(self, resource_type: str, settings: dict, superclasses: list):
        """
            Registers a sub-resource, linking and updating the super-resource accordingly,
            and registers its "sub-sub-resources" recursively
            :param superclasses: List of
            :param resource_type: PascalType
            :param settings:
        """
        settings['schema']['@type']['allowed'] = [resource_type]
        resource_name = Naming.resource(resource_type)
        # We update the values of the parent with ours.
        # We need to do some tricks to not to override allowed in @type in the parent when updating
        for superclass in superclasses:
            new_type_settings_schema = copy.deepcopy(settings['schema'])
            del new_type_settings_schema['@type']
            parent_resource_name = Naming.resource(superclass)
            parent_resource_schema = self.config['DOMAIN'][parent_resource_name]['schema']
            parent_resource_schema.update(new_type_settings_schema)
            parent_resource_schema['@type']['allowed'].append(resource_type)
            # We call directly 'super' so we do not end into an infinite recursion
            self.update_resource(parent_resource_name, self.config['DOMAIN'][parent_resource_name])
        # We register the actual subclass
        # And the subclasses it may have
        url_names = [Naming.resource(superclass) for superclass in superclasses]
        settings['url'] = '{}/{}'.format('/'.join(url_names), resource_name)
        settings['datasource'] = settings['datasource'] if 'datasource' in settings else {}
        settings['datasource']['source'] = Naming.resource(superclasses[0])
        settings['datasource']['filter'] = {'@type': {'$eq': resource_type}}
        self.register_resource(resource_name, settings, copy.deepcopy(superclasses))

    # noinspection PyMethodMayBeStatic
    def update_resource(self, resource, settings):
        """
            It just updates the settings and schema of the resource, without affecting other resources.
        """
        # We need to remove 'datasource' if existed, or eve is not going to generate it well
        settings.pop('datasource', None)
        super().register_resource(resource, settings)

    def _add_resource_url_rules(self, resource, settings):
        if resource in self.config['RESOURCES_USING_DEFAULT_DATABASE']:
            super(DeviceHub, self)._add_resource_url_rules(resource, settings)
        else:
            real_url_prefix = self.config['URL_PREFIX']
            for database in self.config['DATABASES']:
                self.config['URL_PREFIX'] = database
                super(DeviceHub, self)._add_resource_url_rules(resource, settings)
            self.config['URL_PREFIX'] = real_url_prefix
