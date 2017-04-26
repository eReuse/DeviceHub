import copy
from contextlib import suppress
from distutils import version

import validators
from bson import json_util, ObjectId
from bson.errors import InvalidId
from cerberus import errors
from eve.io.mongo import Validator
from eve.utils import config
from flask import current_app as app

from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.utils import coerce_type
from . import errors as dh_errors

ALLOWED_WRITE_ROLES = 'dh_allowed_write_roles'
COERCE_WITH_CONTEXT = 'coerce_with_context'


class DeviceHubValidator(Validator):
    SCALE_AD = ['A', 'B', 'C', 'D']
    SCALE_AE = SCALE_AD + ['E']
    SCALE_0E = ['0'] + SCALE_AE

    special_rules = Validator.special_rules + ('or', COERCE_WITH_CONTEXT, 'move')

    def __init__(self, schema=None, resource=None, allow_unknown=False, transparent_schema_rules=False):
        self._validations = {}
        """Fields that have been already validated"""
        super().__init__(schema, resource, allow_unknown, transparent_schema_rules)

    def _validate(self, document, schema=None, update=False, context=None):
        self._coerce_type(document)
        self._remove_none(document)
        super(DeviceHubValidator, self)._validate(document, schema, update, context)
        if document == self.document:  # I am the top document
            from ereuse_devicehub.resources.device.schema import Device
            if document.get('@type', None) in Device.types and not document.get('placeholder', False):
                self._validate_type_hid('hid', None)
        self._validate_or(self._current)
        return len(self._errors) == 0

    @staticmethod
    def _remove_none(document):
        for field in [f for f in document]:
            if document[field] is None:
                del document[field]

    def _validate_definition(self, definition, field, value):
        """
           Extends _validate_definition by:
           - Removing the null fields, as they equal 'undefined'.
        """
        self._validations[field] = True
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

    def _move(self, to, value, field, _):
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
        """Only the specified roles can write the field."""
        from ereuse_devicehub.resources.account.domain import AccountDomain
        if not AccountDomain.actual['role'].has_role(roles):
            self._error(field, json_util.dumps({'ForbiddenToWrite': self.document}))

    def _validate_or(self, document):
        """At least the field, or any of the others specified, are required."""
        for field_name, definition in self.schema.items():
            if 'or' in definition:
                field_names = set([field_name] + definition['or'])
                if field_names.isdisjoint(document.keys()):
                    self._error(next(iter(field_names)),
                                'You need at least one of the following: {}'.format(field_names))

    @staticmethod
    def _coerce_type(fields):
        """
         A coerce method masked in a validation one, as coerce has some bugs in Cerberus 0.96.

         Warning: Do not read from @type in other validations as this method changes the value.
         """
        # todo move it to a coerce method when Cerberus 0.10 is out
        if fields:
            coerce_type(fields)

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

    def _validate_type_hid(self, field, _):
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
            from ereuse_devicehub.resources.device.domain import DeviceDomain
            # todo this should not be done in the validation. Prove of this is that it needs to be done in
            # register/hooks again for placeholders
            self.document['hid'] = DeviceDomain.hid(self.document['manufacturer'],
                                                    self.document['serialNumber'],
                                                    self.document['model'])
        except KeyError:
            self.document['isUidSecured'] = False
            if '_id' not in self.document:  # We do not validate here the unique constraint of _id
                if 'parent' in self.document:
                    with suppress(KeyError, DeviceNotFound):
                        component = ComponentDomain.get_similar_component(self.document, self.document['parent'])
                        self._error('model', json_util.dumps({'NotUnique': component}))
                else:
                    # If device has no parent and no hid, user needs to: or provide _id or forcing creating it
                    if 'forceCreation' not in self.document or not self.document['forceCreation']:
                        self._error('_id', json_util.dumps({'NeedsId': self.document}))
                        # else: user forces us to create the device, it will be assigned an _id
                        # else: user provided _id. We accept this, however is unsecured.
        else:
            from ereuse_devicehub.resources.device.settings import HID_REGEX
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
        """Internally use. See the super method this one overrides."""
        if not isinstance(value, dict) and not isinstance(value, list):  # todo more broad way?
            super(DeviceHubValidator, self)._validate_data_relation(data_relation, field, value)

    def _validate_device_id(self, validate, field, value):
        from ereuse_devicehub.resources.account.domain import AccountDomain
        if validate and self.resource == 'computer' and AccountDomain.actual['role'] < Role(Role.SUPERUSER):
            # Superusers can create devices setting the _id, for example when importing devices
            if self._get_resource(True, field, value, {}) is None:
                self._error(field, json_util.dumps({'CannotCreateId': self.document}))

    def _validate_type_natural(self, field, value):
        """Validate that the value is a natural; this is, a non-negative integer."""
        self._validate_type_integer(field, value)
        if value < 0:
            self._error(field, errors.ERROR_BAD_TYPE.format('natural (positive integer)'))

    def _validate_type_url(self, field, value):
        """Validate that the value is an URL."""
        if not validators.url(value) and 'localhost' not in value:
            self._error(field, errors.ERROR_BAD_TYPE.format('url'))

    def _validate_type_email(self, field, value):
        """Validate that the value is a correct e-mail."""
        if not validators.email(value):
            self._error(field, errors.ERROR_BAD_TYPE.format('email'))

    def _validate_type_uuid(self, field, value):
        """Validates that the value is an UUID."""
        if not validators.uuid(value):
            self._error(field, errors.ERROR_BAD_TYPE.format('uuid'))

    def _validate_type_version(self, field, value):
        """Validates that the value is a Python strict version."""
        try:
            version.StrictVersion(value)
        except ValueError:
            self._error(field, '{} is not a valid python strict version.'.format(value))

    def _validate_sink(self, nothing, field, value):
        """Order fields by setting a priority value, where the field with lowest value 'sinks' to the bottom."""
        pass

    def _validate_description(self, nothing, field, value):
        """An user-friendly description of the field that can be used in a form."""
        pass

    def _validate_short(self, nothing, field, value):
        """An abbreviation for a field name. Ex: *SerialNumber* -> *S/N*"""
        pass

    # noinspection PyPep8Naming
    def _validate_unitCode(self, nothing, field, value):
        """The UnitCode as in :class:`ereuse_devicehub.resources.schema.UnitCodes`"""
        pass

    def _validate_doc(self, nothing, field, value):
        """Technical description of a field."""
        pass

    def _validate_placeholder_disallowed(self, _, field, device_id):
        from ereuse_devicehub.resources.device.domain import DeviceDomain
        device = DeviceDomain.get_one(device_id)
        if device.get('placeholder', False):
            self._error(field, dh_errors.PLACEHOLDER)

    def _validate_get_from_data_relation_or_create(self, _, field, value):
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
        """Don't expect to GET this value."""
        pass

    def _validate_teaser(self, x, y, z):
        """
        Teaser values are supposed to be shown when the UI shows a minified version of the resource
        (with lesser fields than the usual).
        """
        pass

    def _validate_allowed_description(self, _, field, value):
        """
        Explains each allowed element, useful for selects or dropdowns.

        This provides a dict whose keys are the values a dropdown can get, and whose values are the texts
        the user should see.
        """
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

    def _validate_uid(self, boolean, field, value):
        """The 'uid' is only used to tag a field as an uid. DeviceDomain makes use of this."""
        pass

    def _validate_externalSynthetic(self, boolean, field, value):
        """The 'uid' is only used to tag a field as an uid. DeviceDomain makes use of this."""
        pass

    def _validate_materialized(self, _, field, value):
        """Just to show which values are materialized automatically by DeviceHub. They behave like *readonly*."""
        self._validate_readonly(True, field, value)

    def _validate_required_fields(self, document):
        """Superusers can avoid such restrictions. For example, when importing."""
        from ereuse_devicehub.resources.account.domain import AccountDomain
        if AccountDomain.actual['role'] < Role(Role.SUPERUSER):
            super(DeviceHubValidator, self)._validate_required_fields(document)
