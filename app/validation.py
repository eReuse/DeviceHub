from bson import ObjectId
from eve.io.mongo import Validator
from eve.utils import config
from flask import current_app as app
from bson import json_util
from app.account.user import User
from app.utils import normalize

ALLOWED_WRITE_ROLES = 'dh_allowed_write_roles'
DEFAULT_AUTHOR = 'dh_default_author'
IF_VALUE_REQUIRE = 'dh_if_value_require'
OR = 'dh_or'


class DeviceHubValidator(Validator):
    def _validate_dh_allowed_write_roles(self, roles, field, value):
        if not User.actual['role'].has_role(roles):
            self._error(field, json_util.dumps({'ForbiddenToWrite': self.document}))

    def _validate_dh_or(self, options, field, value):
        role, list_of_names = options
        if User.actual['role'] == role:
            for name in list_of_names:
                if name in self.document:
                    return
            self._error(list_of_names[0], "You need to set one of these: " + str(list_of_names))

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

            datasource, _, _, _ = app.data.datasource(self.resource)
            response = app.data.driver.db[datasource].find_one(query)
            if response:
                from app.device.device import Device
                device = Device.get(response['_id'])
                self._error(field, json_util.dumps({'NotUnique': device}))

    def _validate_type_hid(self, field, value):
        """
        General validation for inserting devices (the name of the function is forced by Cerberus, not a good one).

        - Tries to create hid and validates it.
        - If hid cannot be created:
            - If it has a parent, ensures that the device is unique.
            - If it has not a parent, validates that the device has an user provided _id.
        """
        from app.device.device import Device
        from app.device.exceptions import DeviceNotFound
        try:
            self.document['hid'] = normalize(self.document['manufacturer']) + \
                                   '-' + normalize(self.document['serialNumber']) + \
                                   '-' + normalize(self.document['model'])
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
        if not isinstance(value, dict):  # todo more broad way?
            super(DeviceHubValidator, self)._validate_data_relation(data_relation, field, value)

    def _validate_device_id(self, validate, field, value):
        # if autoincrement:
        if validate and self.resource == 'computer':
            self._validate_unique(True, field, value)
            if len(self._errors) == 0:
                  self._error(field, json_util.dumps({'CannotCreateId': self.document}))

HID_REGEX = '[\w]+-[\w]+-[\w]+'
