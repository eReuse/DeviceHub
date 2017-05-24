from urllib.parse import urlencode

import pyexcel
from assertpy import assert_that
from pydash import at, py_
from pyexcel_webio import _XLSX_MIME, FILE_TYPE_MIME_TABLE
from werkzeug.datastructures import Headers

from ereuse_devicehub.tests import TestStandard


class TestExport(TestStandard):
    def test_export_basic(self):
        """Exports some non-components."""
        computers_id = self.get_fixtures_computers()
        book_dict = self._get_spreadsheet('devices', computers_id)
        assert_that(book_dict).contains_only('Devices')
        first_computer = self.get_and_check('devices', '', computers_id[0])
        assert_that(book_dict['Devices'][1]).contains(*at(first_computer, 'serialNumber', 'model', 'manufacturer'))

    def test_export_computers_wrong_accept(self):
        """Handles queries requesting a wrong file type."""
        url = '/{}/export/devices'.format(self.db1)
        headers = Headers()
        headers.add('Authorization', 'Basic ' + self.token)
        headers.add('Accept', ','.join(['foo', 'bar']))
        response = self.test_client.get(url, headers=headers)
        assert_that(response.status_code).is_equal_to(406)

    def test_export_groups(self):
        """Exports two lots; which generates all devices within them, grouped by lot in every page."""
        computers_id = self.get_fixtures_computers()
        inner_lot = self.get_fixture('groups', 'lot')
        inner_lot['label'] = 'inner lot'
        inner_lot['children']['devices'] = computers_id[0:2]
        inner_lot = self.post_and_check('lots', inner_lot)
        lot = self.get_fixture('groups', 'lot')
        lot['children']['devices'] = computers_id[2:4]
        lot['children']['lots'] = [inner_lot['_id']]  # Inner lot is inside lot
        lot = self.post_and_check('lots', lot)
        book_dict = self._get_spreadsheet('lots', [lot['_id'], inner_lot['_id']])
        assert_that(book_dict).contains_only('inner lot', 'lot')
        # Inner lot has devices 1, 11, and lot has 25 and 35, plus the ones of 'inner lot'
        get_ids = py_().map_(lambda row: row[0])
        assert_that(get_ids(book_dict['inner lot'])).is_equal_to(['Identifier', '1', '11'])
        assert_that(get_ids(book_dict['lot'])).is_equal_to(['Identifier', '1', '11', '25', '35'])

    def _get_spreadsheet(self, resource_name: str, ids: list):
        """Requests an spreadsheet to the server in open xlsx format."""
        url = '/{}/export/{}?{}'.format(self.db1, resource_name, urlencode({'ids': ids}, True))
        headers = Headers()
        headers.add('Authorization', 'Basic ' + self.token)
        headers.add('Accept', ','.join([_XLSX_MIME, FILE_TYPE_MIME_TABLE['ods']]))
        response = self.test_client.get(url, headers=headers)
        self.assert200(response.status_code)
        assert_that(response.content_type).is_equal_to(_XLSX_MIME)
        book = pyexcel.get_book(file_type='xlsx', file_content=response.data)
        return book.to_dict()
