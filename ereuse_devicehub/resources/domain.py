from bson.objectid import ObjectId
from ereuse_devicehub.data_layer import mongo_encode
from ereuse_devicehub.exceptions import StandardError
from ereuse_devicehub.resources.resource import ResourceSettings
from flask import current_app
from passlib.utils import classproperty
from pydash import merge
from pymongo import ReturnDocument
from pymongo.collection import Collection


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
        resource = current_app.data.find_one_raw(cls.resource_name, id_or_filter)
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
        return list(current_app.data.find_raw(cls.resource_name, query_filter))

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
            count += cls.collection.update_one({key: resource_id}, operation).modified_count
        return count

    @classmethod
    @mongo_encode('filter', 'operation')
    def update_many_raw(cls, filter, operation):
        return cls.collection.update_many(filter, operation)

    @classmethod
    @mongo_encode('id_or_filter')
    def update_one_raw(cls, resource_id: str or ObjectId, operation, key='_id'):
        count = cls.collection.update_one({key: resource_id}, operation).matched_count
        if count == 0:
            name = cls.resource_settings._schema.type_name
            raise ResourceNotFound('{} {} cannot be updated as it is not found.'.format(name, resource_id))

    @classmethod
    @mongo_encode('operation', 'extra_query')
    def update_raw_get(cls, ids: str or ObjectId or list, operation: dict, key='_id',
                       return_document=ReturnDocument.AFTER, extra_query={}, **kwargs):
        """Updates the resources and returns them. Set return_document to get the documents before/after the update."""
        resources_id = [ids] if type(ids) is str or type(ids) is ObjectId else ids
        results = []
        for identifier in resources_id:
            q = merge({key: identifier}, extra_query)
            results.append(cls.collection.find_one_and_update(q, operation, return_document=return_document, **kwargs))
        return results

    @classmethod
    @mongo_encode('query')
    def delete_one(cls, query):
        return cls.collection.delete_one(query)

    @classmethod
    @mongo_encode('query')
    def delete_all(cls):
        return cls.collection.drop()

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
        current_app.data.insert(cls.resource_name, document)

    @classproperty
    def resource_name(cls) -> str:
        return cls.resource_settings.resource_name()

    @classproperty
    def collection(cls) -> Collection:
        """Gets the collection in the correct database for the current resource and logged-in account."""

        # (which is the same as the resource)
        try:
            # Collection name is usually the name of the resource, but not always (ex. for components is devices)
            collection_name = cls.resource_settings.datasource['source']
        except AttributeError:
            raise AttributeError('Make sure resource_settings points to the correct subclass of ResourceSettings.')
        else:
            # pymongo(resource) gets the db of our resource and db[resource] the collection
            # This invokes data_layer.current_mongo_prefix, which selects the db
            return current_app.data.pymongo(cls.resource_name).db[collection_name]


class ResourceNotFound(StandardError):
    status_code = 422
