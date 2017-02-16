from unittest import TestCase

from assertpy import assert_that
from bson import ObjectId

from ereuse_devicehub.data_layer import mongo_encode, MongoEncoder
from ereuse_devicehub.tests import TestBase


class TestMongoEncoder(TestCase):
    def test_mongo_encoder(self):
        encoder = MongoEncoder()

        result = encoder.encode_to_mongo({'email': 'logger@ereuse.org'})
        assert_that(result).is_equal_to({'email': 'logger@ereuse.org'})

        result = encoder.encode_to_mongo({'list': [{'set': {1, 2, 3}}, 2, '3', 4]})
        assert_that(result['list']).contains(2, '3', 4)
        assert_that(result['list']).is_type_of(list)
        assert_that(result['list'][0]['set']).is_type_of(list)
        assert_that(result['list'][0]['set']).is_equal_to([1, 2, 3])

        result = encoder.encode_to_mongo([1, 2, {'a': 3, 'b': {4}}])
        assert_that(result).is_type_of(list)
        assert_that(result).contains(1, 2)
        assert_that(result[2]).is_type_of(dict)
        assert_that(result[2]['b']).is_type_of(list)
        assert_that(result[2]['b']).is_equal_to([4])

    def test_objectid(self):
        _id = ObjectId('AAAAAAAAAAAAAAAAAAAAAAAA')
        result = MongoEncoder().encode_to_mongo(_id)
        assert_that(result).is_equal_to(_id)


class TestDataLayer(TestBase):
    def test_mongo_encode(self):
        with self.app.app_context():
            @mongo_encode('a')
            def dummy(a):
                assert_that(a['list']).contains(2, 3, 4)
                assert_that(a['list']).is_type_of(list)
                assert_that(a['list'][0]['set']).is_type_of(list)
                assert_that(a['list'][0]['set']).is_equal_to([1, 2, 3])

            d = {'list': [{'set': {1, 2, 3}}, 2, 3, 4]}
            dummy(d)
