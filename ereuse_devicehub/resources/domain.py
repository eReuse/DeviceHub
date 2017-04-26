from bson.objectid import ObjectId
from flask import current_app
from passlib.utils import classproperty
from pydash import merge
from pymongo import ReturnDocument

from ereuse_devicehub.data_layer import mongo_encode
from ereuse_devicehub.exceptions import StandardError
from ereuse_devicehub.resources.resource import ResourceSettings


class Domain:
    """Provides utility methods to work with resources, like easier access to data-layers. Extend it happily."""
    resource_settings = ResourceSettings
    """Link to the resource settings. Override it linking it with the appropriate subclass"""

    @classmethod
    @mongo_encode('id_or_filter')
    def get_one(cls, id_or_filter: dict or ObjectId or str):
        """
        Obtains a resource.
        :param id_or_filter: An identifier or the filter in Mongo to obtain the resource.
        :raise ResourceNotFound:
        :return:
        """
        resource = current_app.data.find_one_raw(cls.source, id_or_filter)
        if resource is None:
            if type(id_or_filter) is dict:
                text = 'There is no resource matching the query {}'.format(id_or_filter)
            else:
                text = 'The resource with id {} does not exist.'.format(id_or_filter)
            raise ResourceNotFound(text)
        else:
            return resource

    @classmethod
    @mongo_encode('query_filter')
    def get(cls, query_filter: dict) -> list:
        """
        Obtains several resources.
        :param query_filter: A Mongo filter to obtain the resources.
        """
        return list(current_app.data.find_raw(cls.source, query_filter))

    @classmethod
    @mongo_encode('values')
    def get_in(cls, field: str, values: list):
        """The same as get({field: {$in: values}})."""
        return cls.get({field: {'$in': values}})

    @classmethod
    @mongo_encode('operation')
    def update_raw(cls, ids: str or ObjectId or list, operation: dict, key='_id'):
        """
        Sets the properties of a resource using directly the database layer.
        :param ids:
        :param operation: MongoDB update query.
        :return The number of files edited in total
        """
        resources_id = [ids] if type(ids) is str or type(ids) is ObjectId else ids
        count = 0
        for resource_id in resources_id:
            count += current_app.data.driver.db[cls.source].update_one({key: resource_id}, operation).modified_count
        return count

    @classmethod
    @mongo_encode('filter', 'operation')
    def update_many_raw(cls, filter, operation):
        return current_app.data.driver.db[cls.source].update_many(filter, operation)

    @classmethod
    @mongo_encode('id_or_filter')
    def update_one_raw(cls, resource_id: str or ObjectId, operation, key='_id'):
        count = current_app.data.driver.db[cls.source].update_one({key: resource_id}, operation).matched_count
        if count == 0:
            name = cls.resource_settings._schema.type_name
            raise ResourceNotFound('{} {} cannot be updated as it is not found.'.format(name, resource_id))

    @classmethod
    @mongo_encode('operation', 'extra_query')
    def update_raw_get(cls, ids: str or ObjectId or list, operation: dict, key='_id',
                       return_document=ReturnDocument.AFTER, extra_query={}, **kwargs):
        """Updates the resources and returns them. Set *return_document* to get the documents before/after the update."""
        resources_id = [ids] if type(ids) is str or type(ids) is ObjectId else ids
        data = current_app.data.driver.db[cls.source]
        results = []
        for identifier in resources_id:
            query = merge({key: identifier}, extra_query)
            results.append(data.find_one_and_update(query, operation, return_document=return_document, **kwargs))
        return results

    @classmethod
    @mongo_encode('query')
    def delete_one(cls, query):
        return current_app.data.driver.db[cls.source].delete_one(query)

    @classmethod
    @mongo_encode('query')
    def delete_all(cls):
        return current_app.data.driver.db[cls.source].drop()

    @classproperty
    def source(cls):
        try:
            return cls.resource_settings.datasource['source']
        except AttributeError:
            raise AttributeError('Make sure resource_settings points to the correct subclass of ResourceSettings.')

    @classmethod
    def path_for(cls, database: str, identifier: str or ObjectId or int) -> str:
        """Returns the resource path for a given identifier."""
        path = current_app.config['DOMAIN'][cls.resource_settings.resource_name()]['url']
        return '{}/{}/{}'.format(database, path, str(identifier))

    @classmethod
    def url_agent_for(cls, database: str, identifier: str or ObjectId or int):
        """Returns the resource full url as seen for other agents."""
        return '{}/{}'.format(current_app.config['BASE_URL_FOR_AGENTS'], cls.path_for(database, identifier))

    @classmethod
    def insert(cls, document: dict):
        """Inserts a document."""
        current_app.data.insert(cls.source, document)


class ResourceNotFound(StandardError):
    status_code = 422
