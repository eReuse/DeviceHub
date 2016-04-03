from distutils import version

import validators
from bson import json_util
from cerberus import errors
from eve.io.mongo import Validator
from eve.utils import config
from flask import current_app as app
from validators.utils import ValidationFailure

from ereuse_devicehub.resources.account.user import User
from ereuse_devicehub.utils import Naming

ALLOWED_WRITE_ROLES = 'dh_allowed_write_roles'
DEFAULT_AUTHOR = 'dh_default_author'
IF_VALUE_REQUIRE = 'dh_if_value_require'

HID_REGEX = '[\w]+-[\w]+-[\w]+'


# noinspection PyPep8Naming
class DeviceHubValidator(Validator):
    special_rules = Validator.special_rules + ('or',)

    def _validate(self, document, schema=None, update=False, context=None):
        super(DeviceHubValidator, self)._validate(document, schema, update, context)
        self._validate_or(self._current)
        return len(self._errors) == 0

    def _validate_dh_allowed_write_roles(self, roles, field, value):
        if not User.actual['role'].has_role(roles):
            self._error(field, json_util.dumps({'ForbiddenToWrite': self.document}))

    def _validate_or(self, document):
        for field_name, definition in self.schema.items():
            if 'or' in definition:
                field_names = set([field_name] + definition['or'])
                if field_names.isdisjoint(document.keys()):
                    self._error(next(iter(field_names)),
                                'You need at least one of the following: {}'.format(field_names))

    def _validate_dh_if_value_require(self, condition: tuple, field: str, value):
        desired_value, fields = condition
        if value == desired_value:
            if not all(other_field in self.document.keys() for other_field in fields):
                self._error(field, "When {} is {}, you need to send: {}".format(field, desired_value, fields))

    def _is_value_unique(self, unique, field, value, query):
        """
        We override this method to give the ability to show the _id when unique constraint fails.

        We add self.resource validation, as when in used in a dict, unique doesn't work (it is under other resource,
        anyway, so we do not expect it to work)

        We move the logic of unique in the following method.
        """
        if unique and self.resource:
            query[field] = value

            # exclude current document
            if self._id:
                id_field = config.DOMAIN[self.resource]['id_field']
                query[id_field] = {'$ne': self._id}

            # we perform the check on the native mongo driver (and not on
            # app.data.find_one()) because in this case we don't want the usual
            # (for eve) query injection to interfere with this validation. We
            # are still operating within eve's mongo namespace anyway.

            response = app.data.find_one_raw(self.resource, query)
            if response:
                from ereuse_devicehub.resources.device.device import Device
                device = Device.get_one(response['_id'])
                self._error(field, json_util.dumps({'NotUnique': device}))

    def _validate_type_hid(self, field, value):
        """
        General validation for inserting devices (the name of the function is forced by Cerberus, not a good one).

        - Tries to create hid and validates it.
        - If hid cannot be created:
            - If it has a parent, ensures that the device is unique.
            - If it has not a parent, validates that the device has an user provided _id.
        """
        from ereuse_devicehub.resources.device.device import Device
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
                        component = Device.get_similar_component(self.document, self.document['parent'])
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

    def _validate_data_relation(self, data_relation, field, value):
        if not isinstance(value, dict) and not isinstance(value, list):  # todo more broad way?
            super(DeviceHubValidator, self)._validate_data_relation(data_relation, field, value)

    def _validate_device_id(self, validate, field, value):
        if validate and self.resource == 'computer':
            self._validate_unique(True, field, value)
            if len(self._errors) == 0:
                self._error(field, json_util.dumps({'CannotCreateId': self.document}))

    def _validate_type_natural(self, field, value):
        self._validate_type_integer(field, value)
        if value < 0:
            self._error(field, errors.ERROR_BAD_TYPE.format('natural (positive integer)'))

    def _validate_type_url(self, field, value):
        try:
            validators.url.url(value)
        except ValidationFailure:
            self._error(field, errors.ERROR_BAD_TYPE.format('email'))

    def _validate_type_email(self, field, value):
        try:
            validators.email(value)
        except ValidationFailure:
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

    @staticmethod
    def _validate_writeonly(x, y, z):
        """
        Don't expect to GET this value.
        """
        pass

    def _validate_teaser(self, x, y, z):
        pass

    def _validate_excludes(self, other_field: list, field: str, value):
        if other_field in self.document:
            self._error(field, 'Cannot be with {} field.'.format(other_field))

    def _validate_unique_values(self, boolean, field, value):
        if boolean:
            if len(value) != len(set(value)):
                self._error(field, 'There cannot be repetitions')

    def _validate_modifiable(self, boolean, field, value):
        """
        Validates that a value is not modified: once the value has ben set, it cannot be changed.
        :param boolean:
        :param field:
        :param value:
        :return:
        """
        if not boolean:
            if hasattr(self, '_original_document') and self._original_document is not None \
                    and field in self._original_document and value != self._original_document[field]:
                self._error(field, 'You cannot modify this value.')

    def _error(self, field, _error):
        super()._error(field, _error)
        # In DeviceHub, some errors may need to check for other errors, which can cause the same error
        # being showed again. Let's remove duplicates
        # todo do this after using all the errors
        if type(self._errors[field]) is list:
            self._errors[field] = list(set(self._errors[field]))
