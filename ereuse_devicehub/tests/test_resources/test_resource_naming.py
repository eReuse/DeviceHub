from assertpy import assert_that

from ereuse_devicehub.tests import TestBase
from ereuse_devicehub.utils import Naming


class TestResourceNaming(TestBase):
    @staticmethod
    def try_prefix(original_type, prefix, supposed_resource_name):
        """
        :param original_type: The resource type
        :param prefix:
        :param supposed_resource_name: What should the resource name be?
        """
        type_name = Naming.new_type(original_type, prefix)
        equal = original_type if prefix is None else '{}{}{}'.format(prefix, Naming.TYPE_PREFIX, original_type)
        assert_that(type_name).is_equal_to(equal)
        resource_name = Naming.resource(type_name)
        equal = supposed_resource_name if prefix is None else '{}{}{}'.format(prefix, Naming.RESOURCE_PREFIX,
                                                                              supposed_resource_name)
        assert_that(resource_name).is_equal_to(equal)

    def test_prefix(self):
        """
            Tests the creation of prefixes, given a type.
        """
        # Let's try first with a type that doesn't change the number (singular - plural)
        self.try_prefix('Snapshot', 'devices', 'snapshot')
        # Now with a type that can change its number (see RESOURCES_CHANGING_NUMBER in settings)
        self.try_prefix('Event', 'projects', 'events')
        # Finally without prefix
        self.try_prefix('Device', None, 'devices')
        self.try_prefix('Package', None, 'packages')
        self.try_prefix('Lot', None, 'lots')
        self.try_prefix('InputLot', None, 'input-lot')
        self.try_prefix('Place', None, 'places')
