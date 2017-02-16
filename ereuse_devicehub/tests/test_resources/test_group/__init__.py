from assertpy import assert_that
from bson import ObjectId

from ereuse_devicehub.tests import TestStandard
from ereuse_devicehub.utils import Naming


class TestGroupBase(TestStandard):
    PACKAGES = 'packages'
    LOTS = 'lots'
    INPUT_LOT = 'input-lot'
    OUTPUT_LOT = 'output-lot'
    INPUT_LOT_URL = '{}/{}'.format(LOTS, INPUT_LOT)
    OUTPUT_LOT_URL = '{}/{}'.format(LOTS, OUTPUT_LOT)

    def is_parent(self, parent_key: str or ObjectId, parent_resource_name: str, child_key: str or ObjectId,
                  child_resource_name: str):
        """
            Checks if a parent group contains a child group, and otherwise.

            This method suppose that no changes in components have been made to the device after
            setting parenthood.

            Parent key can be both the label and the _id of the parent.
        """
        parent_type = Naming.type(parent_resource_name)

        child, status = self.get(child_resource_name, item=child_key, query='?embedded={"components": true}')
        self.assert200(status)
        assert_that(child).contains('ancestors')

        # parent, status = self.get(parent_resource_name, item=parent_label)
        parent, status = self._get('{}/{}/{}'.format(self.db1, parent_resource_name, parent_key), token=self.token)
        self.assert200(status)
        parent_label = parent['label']
        assert_that(parent).contains('children')

        try:
            # Child does have parent
            assert_that(child['ancestors']).extracting('@type', 'label').contains((parent_type, parent_label))
            for component in child.get('components', []):
                assert_that(component).contains('ancestors')
                assert_that(component['ancestors']).extracting('@type', 'label').contains((parent_type, parent_label))

            # Parent does have child
            assert_that(parent['children']).contains(child_resource_name)
            assert_that(parent['children'][child_resource_name]).contains(child_key)
            # todo materialize children
            # if 'components' in child:  # If the child has components, the father should have relationship to them
            #    assert_that(parent['children']['components']).contains(*pluck(child['components'], '_id'))
        except AssertionError as e:
            raise IsNotAncestor('{} is not a parent of {}'.format(parent_label, str(child_key))) from e

    def is_not_parent(self, parent_label: str, parent_resource_name: str, child_key: str or ObjectId,
                      child_resource_name: str):
        """As `is_parent` but opposite."""
        try:

            self.is_parent(parent_label, parent_resource_name, child_key, child_resource_name)
            raise AssertionError('{} is a parent of {}'.format(parent_label, str(child_key)))
        except IsNotAncestor:
            pass

    def is_grandpa_or_above(self, parent_label: str, parent_resource_name: str, child_key: str or ObjectId,
                            child_resource_name: str):
        child, status = self.get(child_resource_name, item=child_key, query='?embedded={"components": true}')
        self.assert200(status)
        children = child.get('components', []) + [child]
        orphans = []
        for _child in children:
            for ancestor in _child.get('ancestors', []):
                if parent_label in ancestor.get(parent_resource_name, []):
                    break
            else:
                if '_id' in _child:
                    orphans.append(_child['_id'])
                else:
                    orphans.append(_child['label'])
        if len(orphans) > 0:
            text = '{} is not a grandpa or above of {} {}'.format(parent_label, child_resource_name, str(orphans))
            raise IsNotAncestor(text)

    def is_not_grandpa_or_above(self, parent_label: str, parent_resource_name: str, child_key: str or ObjectId,
                                child_resource_name: str):
        try:
            self.is_grandpa_or_above(parent_label, parent_resource_name, child_key, child_resource_name)
        except IsNotAncestor:
            pass
        else:
            raise AssertionError('{} is a grandpa or above of {}'.format(parent_label, str(child_key)))

    def child_does_have_parent(self, parent_label: str, parent_resource_name: str, child_key: str or ObjectId,
                               child_resource_name: str):
        """Use this only when the parent does not exist anymore. Use *is_parent* when possible."""
        child, status = self.get(child_resource_name, item=child_key, query='?embedded={"components": true}')
        self.assert200(status)
        parent_type = Naming.type(parent_resource_name)
        try:
            assert_that(child['ancestors']).extracting('@type', 'label').contains((parent_type, parent_label))
            for component in child.get('components', []):
                assert_that(component).contains('ancestors')
                assert_that(component['ancestors']).extracting('@type', 'label').contains((parent_type, parent_label))
        except AssertionError as e:
            raise IsNotAncestor() from e

    def child_does_not_have_parent(self, parent_label: str, parent_resource_name: str, child_key: str or ObjectId,
                                   child_resource_name: str):
        """Use this only when the parent does not exist anymore. Use *is_parent* when possible."""
        try:
            self.child_does_have_parent(parent_label, parent_resource_name, child_key, child_resource_name)
        except IsNotAncestor:
            pass
        else:
            raise AssertionError('{} is a parent of {}'.format(parent_label, str(child_key)))


class IsNotAncestor(AssertionError):
    pass
