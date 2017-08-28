import sys
from pprint import pprint

import pymongo
from assertpy import assert_that
from flask import json

from ereuse_devicehub.resources.group.group_log.settings import UpdateGroupLogEntry
from ereuse_devicehub.tests import TestStandard
from ereuse_devicehub.utils import Naming


class TestGroupBase(TestStandard):
    PACKAGES = 'packages'
    LOTS = 'lots'
    INPUT_LOT = 'input-lot'
    OUTPUT_LOT = 'output-lot'
    INPUT_LOT_URL = '{}/{}'.format(LOTS, INPUT_LOT)
    OUTPUT_LOT_URL = '{}/{}'.format(LOTS, OUTPUT_LOT)
    PALLETS = 'pallets'

    def is_parent(self, parent_id: str, parent_resource_name: str, child_id: str, child_resource_name: str):
        """
            Checks if a parent group contains a child group, and otherwise.

            This method suppose that no changes in components have been made to the device after
            setting parenthood.
        """
        parent_type = Naming.type(parent_resource_name)

        child = self.get_and_check(child_resource_name, item=child_id, embedded={'components': True})
        assert_that(child).contains('ancestors')

        # parent, status = self.get(parent_resource_name, item=parent_label)
        parent = self.get_and_check(parent_resource_name, item=parent_id)
        parent_id = parent['_id']
        assert_that(parent).contains('children')

        try:
            # Child does have parent
            assert_that(child['ancestors']).extracting('@type', '_id').contains((parent_type, parent_id))
            for component in child.get('components', []):
                assert_that(component).contains('ancestors')
                assert_that(component['ancestors']).extracting('@type', '_id').contains((parent_type, parent_id))

            # Parent does have child
            assert_that(parent['children']).contains(child_resource_name)
            assert_that(parent['children'][child_resource_name]).contains(child['_id'])
            # todo materialize children
            # if 'components' in child:  # If the child has components, the father should have relationship to them
            #    assert_that(parent['children']['components']).contains(*pluck(child['components'], '_id'))
        except AssertionError as e:
            raise IsNotAncestor('{} is not a parent of {}'.format(parent['label'], str(child_id))) from e

    def is_not_parent(self, parent_id: str, parent_resource_name: str, child_id: str, child_resource_name: str):
        """As `is_parent` but opposite."""
        try:

            self.is_parent(parent_id, parent_resource_name, child_id, child_resource_name)
            raise AssertionError('{} is a parent of {}'.format(parent_id, str(child_id)))
        except IsNotAncestor:
            pass

    def is_grandpa_or_above(self, parent_id: str, parent_resource_name: str, child_id: str, child_resource_name: str):
        child, status = self.get(child_resource_name, item=child_id, embedded={'components': True})
        parent = self.get_and_check(parent_resource_name, item=parent_id)
        self.assert200(status)
        children = child.get('components', []) + [child]
        orphans = []
        for _child in children:
            for ancestor in _child.get('ancestors', []):
                if parent['_id'] in ancestor.get(parent_resource_name, []):
                    break
            else:
                orphans.append(_child['_id' if '_id' in _child else 'label'])
        if len(orphans) > 0:
            text = '{} is not a grandpa or above of {} {}'.format(parent_id, child_resource_name, str(orphans))
            raise IsNotAncestor(text)

    def is_not_grandpa_or_above(self, parent_id: str, parent_resource_name: str, child_id: str,
                                child_resource_name: str):
        try:
            self.is_grandpa_or_above(parent_id, parent_resource_name, child_id, child_resource_name)
        except IsNotAncestor:
            pass
        else:
            raise AssertionError('{} is a grandpa or above of {}'.format(parent_id, str(child_id)))

    def child_does_have_parent(self, parent_id: str, parent_resource_name: str, child_id: str,
                               child_resource_name: str):
        """Use this only when the parent does not exist anymore. Use *is_parent* when possible."""
        child = self.get_and_check(child_resource_name, item=child_id, embedded={'components': True})
        parent_type = Naming.type(parent_resource_name)
        try:
            assert_that(child['ancestors']).extracting('@type', '_id').contains((parent_type, parent_id))
            for component in child.get('components', []):
                assert_that(component).contains('ancestors')
                assert_that(component['ancestors']).extracting('@type', '_id').contains((parent_type, parent_id))
        except AssertionError as e:
            raise IsNotAncestor() from e

    def child_does_not_have_parent(self, parent_id: str, parent_resource_name: str, child_id: str,
                                   child_resource_name: str):
        """Use this only when the parent does not exist anymore. Use *is_parent* when possible."""
        try:
            self.child_does_have_parent(parent_id, parent_resource_name, child_id, child_resource_name)
        except IsNotAncestor:
            pass
        else:
            raise AssertionError('{} is a parent of {}'.format(parent_id, str(child_id)))

    def assert_last_log_entry(self, parent_id: str, parent_type: str, added: dict = None, removed: dict = None):
        """Asserts that the last log entry is correctly set."""
        parent = self.get_and_check(Naming.resource(parent_type), item=parent_id)
        where = {'parent': {'_id': parent['_id'], '@type': parent_type}, '@type': UpdateGroupLogEntry.type_name}
        sort = [('_created', pymongo.DESCENDING)]
        params = {'where': json.dumps(where), 'sort': json.dumps(sort), 'max_results': '1'}
        try:
            response = self.get_and_check('group-log-entry', params=params)
            entry = response['_items'][0]
            if added:
                assert_that(added).is_subset_of(entry.get('added', None))
            if removed:
                assert_that(removed).is_subset_of(entry.get('removed', None))
        except Exception as e:
            # There is a really strange bug that happens few times when running (not debugging!) tests
            # The following lines can help trace it when it happens
            # Note that they must be deleted once the bug has been resolved
            pprint(parent_id, stream=sys.stderr)
            pprint(parent_type, stream=sys.stderr)
            pprint(added, stream=sys.stderr)
            pprint(removed, stream=sys.stderr)
            pprint(response, stream=sys.stderr)
            with self.app.test_request_context('/{}/devices'.format(self.db1)):
                pprint(list(self.app.data.find_raw('group-log-entry', {})))
            pprint(self.get_and_check('group-log-entry'), stream=sys.stderr)
            raise AssertionError('Last log entry is not as described.') from e


class IsNotAncestor(AssertionError):
    pass
