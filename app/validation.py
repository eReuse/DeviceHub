from bson import ObjectId
from eve.io.mongo import Validator
from eve.utils import config
from flask import current_app as app
from bson import json_util

from app.account.user import User
from app.device.settings import HID_REGEX
from app.utils import normalize

ALLOWED_WRITE_ROLES = 'dh_allowed_write_roles'
DEFAULT_AUTHOR = 'dh_default_author'
OR = 'dh_or'


class DeviceHubValidator(Validator):
    def _validate_dh_allowed_write_roles(self, roles, field, value):
        if not User.actual['role'] in roles:
            self._error(field, "You do not have permission to write field " + field + ".")

    def _validate_dh_or(self, list_of_names, field, value):
        for name in list_of_names:
            if name in self.document:
                return
        self._error(list_of_names[0], "You need to set one of these: " + str(list_of_names))

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
        from app.device.device import Device
        from app.device.exceptions import DeviceNotFound
        try:
            self.document['hid'] = normalize(self.document['manufacturer']) + '-' + normalize(self.document['serialNumber'])
        except KeyError:
            del self.document['hid']
            if 'pid' not in self.document and 'parent' in self.document:  # if pid exists
                try:
                    component = Device.get_similar_component(self.document, ObjectId(self.document['parent']))
                    self._error('model', json_util.dumps({'NotUnique': component}))
                except (KeyError, DeviceNotFound):
                    self.document['isUidSecured'] = False
        else:
            self._validate_regex(HID_REGEX, field, self.document['hid'])
            self._validate_unique(True, field, self.document['hid'])
