from assertpy import assert_that
from bson import ObjectId

from ereuse_devicehub.tests import TestStandard
from ereuse_devicehub.utils import Naming


class TestGroupBase(TestStandard):
    PACKAGES = 'packages'
    LOTS = 'lots'

    def is_parent(self, parent_label: str, parent_resource_name: str, child_key: str or ObjectId,
                  child_resource_name: str):
        """Checks if a parent group contains a child group, and otherwise."""
        # Child does have parent
        child, status = self.get(child_resource_name, item=child_key)
        self.assert200(status)
        assert_that(child).contains('ancestors')
        parent_type = Naming.type(parent_resource_name)
        assert_that(child['ancestors']).extracting('@type', 'label').contains((parent_type, parent_label))

        # Parent does have child
        parent, status = self.get(parent_resource_name, '', parent_label)
        self.assert200(status)
        assert_that(parent).contains('children')
        assert_that(parent['children']).contains(child_resource_name)
        assert_that(parent['children'][child_resource_name]).contains(child)

    def is_not_parent(self, parent_label: str, parent_resource_name: str, child_key: str or ObjectId,
                      child_resource_name: str):
        """As `is_parent` but opposite."""
        # Child does not have parent
        child, status = self.get(child_resource_name, '', child_key)
        self.assert200(status)
        assert_that(child).contains('ancestors')
        clause = (parent_resource_name, parent_label)
        assert_that(child['ancestors']).extracting('@type', 'label').does_not_contain(clause)

        # Parent does not have child
        parent, _ = self.get(parent_resource_name, item=parent_label)
        self.assert200(status)
        children_of_type = parent.get('children', {}).get(child_resource_name, None)
        assert_that(child_key).is_not_in(children_of_type)

    def is_grandpa_or_above(self, parent_label: str, parent_resource_name: str, child_key: str or ObjectId,
                            child_resource_name: str):
        child, _ = self.get(child_resource_name, item=child_key)
        for ancestor in child.get('ancestors', []):
            if parent_label in ancestor.get(parent_resource_name, []):
                break
        else:
            raise self.failureException('{} is not a grandpa or above of {}'.format(parent_label, str(child_key)))

    def is_not_grandpa_or_above(self, parent_label: str, parent_resource_name: str, child_key: str or ObjectId,
                                child_resource_name: str):
        try:
            self.is_grandpa_or_above(parent_label, parent_resource_name, child_key, child_resource_name)
        except AssertionError:
            pass
        else:
            raise self.failureException('{} is a grandpa or above of {}'.format(parent_label, str(child_key)))
