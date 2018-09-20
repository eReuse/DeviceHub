from assertpy import assert_that

from ereuse_devicehub.tests import TestStandard


class TestDeviceEventUpdate(TestStandard):
    def test_creation(self):
        computers_id = self.get_fixtures_computers()
        update = {
            '@type': 'devices:Update',
            'devices': computers_id,
            'margin': 'foo',
            'price': '1.3',
            'partners': 'baz',
            'invoiceRetailerId': 'fff',
            'eTag': 'DT-494949'
        }
        update = self.post_201(self.DEVICE_EVENT_UPDATE, update)
        assert_that(update).has_margin('foo')
        assert_that(update).has_price('1.3')
        assert_that(update).has_partners('baz')
        assert_that(update).has_invoiceRetailerId('fff')
        assert_that(update).has_eTag('DT-494949')
