import re

import inflection
from bson import objectid, ObjectId

from flask import json

from app.app import app
from app.exceptions import InnerRequestError, StandardError
from app.utils import normalize
from .exceptions import HidError
from .settings import HID_REGEX


class Device:
    @staticmethod
    def normalize_and_compute_hid(device: dict) -> int:
        try:
            device['hid'] = normalize(device['manufacturer']) + '-' + normalize(device['serialNumber'])
        except KeyError as e:
            raise HidError('Device value ' + str(e) + ' does not exist.')
        if not re.compile(HID_REGEX).match(device['hid']):
            raise HidError('Manufacturer or SerialNumber variables do not led creating a valid HID')
        return device['hid']

    @staticmethod
    def get_device_by_hid(device: dict) -> dict:
        from flask import request
        response = app.test_client().get('devices/' + device['hid'], environ_base={'HTTP_AUTHORIZATION':
                                                                                       request.headers.environ[
                                                                                           'HTTP_AUTHORIZATION']})
        data = json.loads(response.data)
        if response._status_code == 404:
            raise DeviceNotFound()
        elif response._status_code != 200:  # statusCode
            raise InnerRequestError(response._status_code, data['_error']['message'])
        else:
            data['_id'] = ObjectId(data['_id'])
            return data

    @staticmethod
    def get_parent(_id: objectid) -> dict or None:
        parent = app.data.driver.db['devices'].find_one({'components': {'$in': [_id]}})
        if parent is None:
            raise DeviceNotFound()
        else:
            return parent

    @staticmethod
    def seem_equal(x: dict, y: dict) -> bool:
        if id(x) == id(y):
            return True
        elif 'hid' in x and 'hid' in y and x['hid'] == y['hid']:
            return True
        elif 'pid' in x and 'pid' in y and x['pid'] == y['pid']:
            return True
        elif 'hid' not in x and 'hid' not in y and 'pid' not in x and 'pid' not in y and \
                'model' in x and 'model' in y and x['model'] == y['model']:
            return True
        return False
        #  todo improve. What happens for non-hid and non-pid devices?

    @staticmethod
    def difference(list_to_remove_devices_from, checking_list):
        """
        Computes the difference between two lists of devices.

        To compute the difference the position of the parameters is important
        :param list_to_remove_devices_from:
        :param checking_list:
        :return:
        """
        difference = []
        for x in list_to_remove_devices_from:
            found = False
            for y in checking_list:
                if Device.seem_equal(x, y):
                    found = True
            if not found:
                difference.append(x)
        return difference

    @staticmethod
    def get_device_by_id(_id: ObjectId) -> dict:
        return app.data.driver.db['devices'].find_one({'_id': _id})


class DeviceNotFound(StandardError):
    status_code = 401
