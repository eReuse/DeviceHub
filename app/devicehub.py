import copy
import pkgutil
from importlib import import_module

import inflection
from eve import Eve
from eve.flaskapp import RegexConverter
from eve.io.mongo import Mongo, GridFSMediaStorage, Validator
from eve.logging import RequestFilter

from app.schema import ResourceSettings
from app.utils import Naming


class DeviceHub(Eve):
    def register_resource(self, resource: str, settings: ResourceSettings):
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
        self.load_all_settings(settings)

        for sub_resource_settings in settings.sub_resources():
            self.register_resource(sub_resource_settings.resource_name(), sub_resource_settings)
        super().register_resource(resource, settings())



    def load_all_settings(self, settings):
        module = settings.__module__.split('.')
        modules = []
        del module[-1]
        for loader, module_name, is_pkg in pkgutil.walk_packages('.'.join(module)):
            modules.append(import_module('.{}.settings'.format(module_name), '.'.join(module)))
        a = 2

    def _add_resource_url_rules(self, resource, settings):
        if resource in self.config['RESOURCES_USING_DEFAULT_DATABASE']:
            super(DeviceHub, self)._add_resource_url_rules(resource, settings)
        else:
            real_url_prefix = self.config['URL_PREFIX']
            for database in self.config['DATABASES']:
                self.config['URL_PREFIX'] = database
                super(DeviceHub, self)._add_resource_url_rules(resource, settings)
            self.config['URL_PREFIX'] = real_url_prefix
