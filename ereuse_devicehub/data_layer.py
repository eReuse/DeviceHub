import copy
import inspect

from bson.objectid import ObjectId
from eve.io.mongo import Mongo, MongoJSONEncoder
from flask import current_app
from pydash import transform
from pymongo.cursor import Cursor

from ereuse_devicehub.resources.account.role import Role


class MongoEncoder:
    def encode_to_mongo(self, query) -> dict:
        _type = type(query)
        if _type is dict or _type is list:
            return transform(query, self._encode_to_mongo_transform, _type())
        else:
            return query

    def _encode_to_mongo_transform(self, acc, value, key, subdict):
        # Transform the values here
        if type(value) is set:
            value = list(value)
        if issubclass(type(value), list) or issubclass(type(value), dict):
            value = self.encode_to_mongo(value)

        # Set the values here
        # Mongo accepts only list or dict as containers
        if type(acc) is list:
            acc.append(value)
        else:
            acc[key] = value


def mongo_encode(*args_to_transform):
    """Decorator for MongoEncoder.encode_to_mongo"""

    def decorator(function):
        keys, *_ = inspect.getfullargspec(function)

        def wrapper(*args, **kwargs):
            new_args = list(args)
            new_kwargs = copy.copy(kwargs)
            for arg in args:
                i = args.index(arg)
                if keys[i] in args_to_transform:
                    new_args[i] = current_app.mongo_encoder.encode_to_mongo(arg)
            for key in args_to_transform:
                if key in kwargs:
                    new_kwargs[key] = current_app.mongo_encoder.encode_to_mongo(kwargs[key])
            return function(*new_args, **new_kwargs)

        return wrapper

    return decorator


class DhMongoJSONEncoder(MongoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Role):
            return str(obj)
        return super().default(obj)


class DataLayer(Mongo):
    json_encoder_class = DhMongoJSONEncoder

    def current_mongo_prefix(self, resource=None):
        """
        Overrides the default Eve's database selection process, by forcing the resources that use the default database
        settings, to effectively use the default database, regardless of any other setting

        By default, eve sets maximum priority to the database manually set by set_mongo_prefix when we get it from the
        URL.
        :param resource:
        :return:
        """
        if resource is None or not current_app.config['DOMAIN'][resource]['use_default_database']:
            return super(DataLayer, self).current_mongo_prefix(resource)
        else:
            return 'MONGO'

    def aggregate(self, resource, pipeline):
        datasource, *_ = self.datasource(resource)
        return list(self.pymongo(resource).db[datasource].aggregate(pipeline))

    @mongo_encode('query_filter')
    def find_raw(self, resource, query_filter) -> Cursor:
        datasource, *_ = self.datasource(resource)
        return self.pymongo(resource).db[datasource].find(query_filter)

    @mongo_encode('id_or_query')
    def find_one_raw(self, resource, id_or_query: ObjectId or dict or str):
        if type(id_or_query) is dict:
            datasource, *_ = self.datasource(resource)
            return self.pymongo(resource).db[datasource].find_one(id_or_query)
        else:
            return super(DataLayer, self).find_one_raw(resource, id_or_query)

    @mongo_encode('doc_or_docs')
    def insert(self, resource, doc_or_docs):
        return super().insert(resource, doc_or_docs)

    @mongo_encode('updates', 'original')
    def update(self, resource, id_, updates, original):
        return super().update(resource, id_, updates, original)

    @mongo_encode('document', 'original')
    def replace(self, resource, id_, document, original):
        return super().replace(resource, id_, document, original)

    def drop_dtabases(self):
        self.pymongo().db.dropDatabases()
