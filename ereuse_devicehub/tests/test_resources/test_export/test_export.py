from urllib.parse import urlencode

import pyexcel
from assertpy import assert_that
from ereuse_devicehub.tests import TestStandard
from pydash import at
from pyexcel_webio import _XLSX_MIME, FILE_TYPE_MIME_TABLE
from werkzeug.datastructures import Headers


class TestExport(TestStandard):
    def test_export_computers_place(self):
        computers_id = self.get_fixtures_computers()
        place = self.get_fixture(self.PLACES, 'place')
        place['children'] = {'devices': [computers_id[0]]}
        self.post_and_check(self.PLACES, place)
        db, *_ = self.app.config['DATABASES']
        url = '/{}/export/devices?{}'.format(db, urlencode({'ids': computers_id, 'groupBy': 'Actual place'}, True))
        headers = Headers()
        headers.add('Authorization', 'Basic ' + self.token)
        headers.add('Accept', ','.join([_XLSX_MIME, FILE_TYPE_MIME_TABLE['ods']]))
        response = self.test_client.get(url, headers=headers)
        self.assert200(response.status_code)
        assert_that(response.content_type).is_equal_to(_XLSX_MIME)
        book = pyexcel.get_book(file_type='xlsx', file_content=response.data)
        book_dict = book.to_dict()
        # assert_that(book_dict).contains(place['label'])
        first_computer, _ = self.get('devices', '', computers_id[0])
        # assert_that(book_dict[place['label']][1]).contains(*at(first_computer, 'serialNumber', 'model', 'manufacturer'))

    def test_export_computers_wrong_accept(self):
        db, *_ = self.app.config['DATABASES']
        url = '/{}/export/devices?{}'.format(db, urlencode({'groupBy': 'Actual place'}, True))
        headers = Headers()
        headers.add('Authorization', 'Basic ' + self.token)
        headers.add('Accept', ','.join(['foo', 'bar']))
        response = self.test_client.get(url, headers=headers)
        assert_that(response.status_code).is_equal_to(406)

