from bson.objectid import ObjectId
from eve.io.mongo import Mongo
from flask import current_app


class DataLayer(Mongo):
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

    def find_raw(self, resource, query_filter):
        datasource, *_ = self.datasource(resource)
        return list(self.pymongo(resource).db[datasource].find(query_filter))

    def find_one_raw(self, resource, id_or_query: ObjectId or dict or str):
        if type(id_or_query) is dict:
            datasource, *_ = self.datasource(resource)
            return self.pymongo(resource).db[datasource].find_one(id_or_query)
        else:
            return super(DataLayer, self).find_one_raw(resource, id_or_query)
