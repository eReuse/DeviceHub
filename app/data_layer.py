from bson import ObjectId
from eve.io.mongo import Mongo
from flask import current_app


class DataLayer(Mongo):
    def current_mongo_prefix(self, resource=None):
        """
        Overrides the default Eve's database selection process, by forcing the resources in RESOURCES_USING_DEFAULT_DATABASE
        settings, to effectively use the default database, regardless of any other setting

        By default, eve sets maximum priority to the database manually set by set_mongo_prefix when we get it from the
        URL.
        :param resource:
        :return:
        """
        if resource in current_app.config['RESOURCES_USING_DEFAULT_DATABASE']:
            return 'MONGO'
        else:
            return super(DataLayer, self).current_mongo_prefix(resource)

    def aggregate(self, resource, pipeline):
        datasource, *_ = self.datasource(resource)
        return self.pymongo(resource).db[datasource].aggregate(pipeline)

    def find_raw(self, resource, query):
        datasource, *_ = self.datasource(resource)
        return self.pymongo(resource).db[datasource].find(query)

    def find_one_raw(self, resource, id_or_query: ObjectId or dict or str):
        if type(id_or_query) is dict:
            datasource, *_ = self.datasource(resource)
            return self.pymongo(resource).db[datasource].find_one(id_or_query)
        else:
            return super(DataLayer, self).find_one_raw(resource, id_or_query)
