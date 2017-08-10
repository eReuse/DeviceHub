from urllib.parse import urlencode

from assertpy import assert_that
from bs4 import BeautifulSoup
from werkzeug.datastructures import Headers

from ereuse_devicehub.tests import TestStandard


class TestDeliveryNote(TestStandard):
    def test_delivery_note(self):
        """
        Test requesting a delivery note for some dummy
        computers and performing some wrong requests.
        """
        # Let's get a valid delivery note
        ids = self.get_fixtures_computers()  # We create computers
        headers = Headers()
        # Note that we don't set the 'Accept' header
        # because delivery-note can only answer with one file type
        headers.add('Authorization', 'Basic ' + self.token)
        # We can't easily check the contents of the pdf
        # But with the argument 'debug' the server answers with an HTML version
        # Note that the PDF generator takes the HTML version and makes a PDF from it
        # So debugging the HTML version we ensure it will be ok for the PDF
        url = '/{}/documents/delivery-note?{}'.format(self.db1, urlencode({'ids': ids, 'debug': True}, True))
        response = self.test_client.get(url, headers=headers)
        self.assert200(response.status_code)
        html = BeautifulSoup(response.data, 'lxml')
        tables = html.find_all('table')
        # 2 tables; the one stating info about the delivery
        # and one and the one with devices
        assert_that(tables).is_length(2)
        # Let's check that the devices are printed in the second table
        # Let's check the second table, which has the devices printed
        rows = tables[1].find_all('tr')
        # Length is 5: 1 for the headers and 4, which is the number
        # of computers self.get_fixtures_computers() creates
        assert_that(rows).is_length(5)
        # Header row
        fields = rows[0].find_all('th')
        assert_that(fields[0].text).is_equal_to('System ID')
        assert_that(fields[1].text).is_equal_to('Type')
        assert_that(fields[2].text).is_equal_to('S/N')
        # Let's check that at least the first computer is printed
        cells = rows[1].find_all('td')
        # Note there are printed newlines (\n) so we use contains not equals
        assert_that(cells[0].text).contains('1')
        assert_that(cells[1].text).contains('Computer')
        assert_that(cells[2].text).contains('86SXQ-0000029')

        # For the same input, let's get the actual PDF
        # So we ensure that the PDF generator works without throwing errors
        # Note the missing 'debug' argument this time
        url = '/{}/documents/delivery-note?{}'.format(self.db1, urlencode({'ids': ids}, True))
        response = self.test_client.get(url, headers=headers)
        self.assert200(response.status_code)
        assert_that(response.content_type).is_equal_to('application/pdf')

        # If we don't pass any 'ids' as arguments it won't work
        url = '/{}/documents/delivery-note'.format(self.db1)
        response = self.test_client.get(url, headers=headers)
        self.assert422(response.status_code)
