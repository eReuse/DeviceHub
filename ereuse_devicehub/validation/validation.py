import copy
from distutils import version

import validators
from bson import json_util, ObjectId
from bson.errors import InvalidId
from cerberus import errors
from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.utils import Naming, coerce_type
from eve.io.mongo import Validator
from eve.utils import config
from flask import current_app as app

from . import errors as dh_errors

ALLOWED_WRITE_ROLES = 'dh_allowed_write_roles'
DEFAULT_AUTHOR = 'dh_default_author'
IF_VALUE_REQUIRE = 'dh_if_value_require'
COERCE_WITH_CONTEXT = 'coerce_with_context'

HID_REGEX = '[\w]+-[\w]+-[\w]+'


class DeviceHubValidator(Validator):
    SCALE_AD = ['A', 'B', 'C', 'D']
    special_rules = Validator.special_rules + ('or', COERCE_WITH_CONTEXT, 'move')

    def __init__(self, schema=None, resource=None, allow_unknown=False, transparent_schema_rules=False):
        self._validations = {}
        """Fields that have been already validated"""
        super().__init__(schema, resource, allow_unknown, transparent_schema_rules)

    def _validate(self, document, schema=None, update=False, context=None):
        self._coerce_type(document)
        super(DeviceHubValidator, self)._validate(document, schema, update, context)
        self._validate_or(self._current)
        return len(self._errors) == 0

    """
       Removes a null field (as they equal 'undefined' ones)
    """

    def _validate_definition(self, definition, field, value):
        self._validations[field] = True
        if value is None:
            # We change this from Python-eve. For us, null values equal undefined fields and they are silently removed
            del self._current[field]
            return
        if 'move' in definition:
            self._move(definition['move'], value, field, definition)
            return  # The actual field has been moved, so there is no value any more to validate
        if COERCE_WITH_CONTEXT in definition:
            value = self._validate_coerce_with_context(definition['coerce_with_context'], field, value)
            self._current[field] = value
        super()._validate_definition(definition, field, value)

    def _validate_coerce_with_context(self, coerce, field, value):
        """Like coerce, but adds parameters to know the context, like the field and the full document."""
        try:
            value = coerce(value, field, self._current, self.schema)
        except (TypeError, ValueError):
            self._error(field, errors.ERROR_COERCION_FAILED.format(field))
        return value

    def _move(self, to, value, field, definition):
        """
        Moves one field to another one.

        :param to: Destination field. It can be 'readonly', as it will be ignored.
        """
        self._current[to] = value
        if self._validations.get(field) or field not in self.document:  # If the field was already validated
            other_definition = copy.deepcopy(self.schema.get(to))  # We do not affect original definition
            other_definition.pop('readonly', None)  # Otherwise we won't be able to 'paste' it
            self._validate_definition(other_definition, to, value)  # As the value changed we need to re-do it
        del self._current[field]

    def _validate_dh_allowed_write_roles(self, roles, field, value):
        from ereuse_devicehub.resources.account.domain import AccountDomain
        if not AccountDomain.actual['role'].has_role(roles):
            self._error(field, json_util.dumps({'ForbiddenToWrite': self.document}))

    def _validate_or(self, document):
        for field_name, definition in self.schema.items():
            if 'or' in definition:
                field_names = set([field_name] + definition['or'])
                if field_names.isdisjoint(document.keys()):
                    self._error(next(iter(field_names)),
                                'You need at least one of the following: {}'.format(field_names))

    def _coerce_type(self, fields):
        """
         A coerce method masked in a validation one, as coerce has some bugs in Cerberus 0.96.

         Warning: Do not read from @type in other validations as this method changes the value.
         """
        # todo move it to a coerce method when Cerberus 0.10 is out
        if fields:
            coerce_type(fields)

    def _validate_dh_if_value_require(self, condition: tuple, field: str, value):
        desired_value, fields = condition
        if value == desired_value:
            if not all(other_field in self.document.keys() for other_field in fields):
                self._error(field, "When {} is {}, you need to send: {}".format(field, desired_value, fields))

    def _get_resource(self, unique, field, value, query):
        if unique and self.resource:
            query[field] = value

            # exclude current document
            if self._id:
                id_field = config.DOMAIN[self.resource]['id_field']
                query[id_field] = {'$ne': self._id}

            return app.data.find_one_raw(self.resource, query)
        else:
            return None

    def _is_value_unique(self, unique, field, value, query):
        """
        We override this method to give the ability to show the _id when unique constraint fails.

        We add self.resource validation, as when in used in a dict, unique doesn't work (it is under other resource,
        anyway, so we do not expect it to work)

        We move the logic of unique in the following method.
        """
        response = self._get_resource(unique, field, value, query)
        if response:
            self._error(field, json_util.dumps({'NotUnique': response}))

    def _validate_type_hid(self, field, value):
        """
        General validation for inserting devices (the name of the function is forced by Cerberus, not a good one).

        - Tries to create hid and validates it.
        - If hid cannot be created:
            - If it has a parent, ensures that the device is unique.
            - If it has not a parent, validates that the device has an user provided _id.
        """
        from ereuse_devicehub.resources.device.component.domain import ComponentDomain
        from ereuse_devicehub.resources.device.exceptions import DeviceNotFound
        try:
            self.document['hid'] = Naming.url_word(self.document['manufacturer']) + \
                                   '-' + Naming.url_word(self.document['serialNumber']) + \
                                   '-' + Naming.url_word(self.document['model'])
        except KeyError:
            del self.document['hid']
            self.document['isUidSecured'] = False
            if '_id' not in self.document:  # We do not validate here the unique constraint of _id
                if 'parent' in self.document:
                    try:
                        component = ComponentDomain.get_similar_component(self.document, self.document['parent'])
                        self._error('model', json_util.dumps({'NotUnique': component}))
                    except (KeyError, DeviceNotFound):
                        pass
                else:
                    # If device has no parent and no hid, user needs to: or provide _id or forcing creating it
                    if 'forceCreation' not in self.document or not self.document['forceCreation']:
                        self._error('_id', json_util.dumps({'NeedsId': self.document}))
                        # else: user forces us to create the device, it will be assigned an _id
                        # else: user provided _id. We accept this, however is unsecured.
        else:
            self._validate_regex(HID_REGEX, field, self.document['hid'])
            self._validate_unique(True, field, self.document['hid'])

    def _validate_type_databases(self, field, databases):
        """Databases are a unique list of values (a set without 'set' for mongo/json compatibilities). Admins can only
        create accounts within their databases."""
        self._validate_type_list(field, databases)
        if len(databases) != len(set(databases)):
            self._error(field, json_util.dumps({'DuplicatedDatabases': 'Databases are duplicated'}))
        from ereuse_devicehub.resources.account.domain import AccountDomain
        if AccountDomain.actual['role'] < Role.SUPERUSER and \
                not set(databases).issubset(set(AccountDomain.actual['databases'])):
            self._error(field, json_util.dumps(dh_errors.not_enough_privilege))

    def _validate_data_relation(self, data_relation, field, value):
        if not isinstance(value, dict) and not isinstance(value, list):  # todo more broad way?
            super(DeviceHubValidator, self)._validate_data_relation(data_relation, field, value)

    def _validate_device_id(self, validate, field, value):
        from ereuse_devicehub.resources.account.domain import AccountDomain
        if validate and self.resource == 'computer' and AccountDomain.actual['role'] < Role(Role.SUPERUSER):
            # Superusers can create devices setting the _id, for example when importing devices
            if self._get_resource(True, field, value, {}) is None:
                self._error(field, json_util.dumps({'CannotCreateId': self.document}))

    def _validate_type_natural(self, field, value):
        self._validate_type_integer(field, value)
        if value < 0:
            self._error(field, errors.ERROR_BAD_TYPE.format('natural (positive integer)'))

    def _validate_type_url(self, field, value):
        if not validators.url(value):
            self._error(field, errors.ERROR_BAD_TYPE.format('email'))

    def _validate_type_email(self, field, value):
        if not validators.email(value):
            self._error(field, errors.ERROR_BAD_TYPE.format('email'))

    def _validate_type_version(self, field, value):
        try:
            version.StrictVersion(value)
        except ValueError:
            self._error(field, '{} is not a valid python strict version.'.format(value))

    def _validate_sink(self, nothing, field, value):
        pass

    def _validate_description(self, nothing, field, value):
        pass

    def _validate_unitCode(self, nothing, field, value):
        pass

    def _validate_doc(self, nothing, field, value):
        pass

    def _validate_get_from_data_relation_or_create(self, nothing, field, value):
        """
        Python-eve is incapable of serializing to objectid when type==[objectid, dict], rejecting the entering string.
        To make it work we add [objectid, dict, string] so the entering string is accepted and then we perform
        the conversion ourselves here.
        """
        if type(value) is not dict:
            try:
                self._current[field] = ObjectId(value)
            except InvalidId as error:
                self._error(field, str(error))

    def _validate_label(self, nothing, field, value):
        pass

    @staticmethod
    def _validate_writeonly(x, y, z):
        """
        Don't expect to GET this value.
        """
        pass

    def _validate_teaser(self, x, y, z):
        pass

    def _validate_excludes(self, other_field: list, field: str, value):
        """
        "Field A and field B cannot have both values."

        A field that is using the default value is treated as it is not using value at all. This method
        presupposes that values cannot be None.
        :param other_field:
        :param field:
        :param value:
        :return:
        """
        if other_field in self.document:
            if self.document[other_field] != self.schema[other_field].get('default', None) \
                    and value != self.schema[field].get('default', None):
                self._error(field, 'Cannot be with {} field.'.format(other_field))

    def _validate_unique_values(self, boolean, field, value):
        if boolean:
            if len(value) != len(set(value)):
                self._error(field, 'There cannot be repetitions')

    def _validate_modifiable(self, boolean, field, value):
        """
        Validates that a value is not modified: once the value has ben set, it cannot be changed.
        """
        if not boolean:
            if hasattr(self, '_original_document') and self._original_document is not None \
                    and field in self._original_document and value != self._original_document[field]:
                self._error(field, 'You cannot modify this value.')

    def _validate_materialized(self, _, field, value):
        """
        Just to show which values are materialized. They behave like *readonly*.
        """
        self._validate_readonly(True, field, value)
