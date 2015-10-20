from bson import objectid, ObjectId
from flask import json
from app.app import app
from app.exceptions import InnerRequestError
from .exceptions import HidError
import re
from .settings import HID_REGEX

__author__ = 'Xavier Bustamante Talavera'


class Device:
    @staticmethod
    def compute_hid(device: dict) -> int:
        try:
            device['hid'] = device['manufacturer'] + '-' + device['serialNumber']
        except KeyError as e:
            raise HidError('Device value ' + str(e) + ' does not exist.')
        if not re.compile(HID_REGEX).match(device['hid']):
            raise HidError('Manufacturer or SerialNumber variables do not led creating a valid HID')
        return device['hid']

    @staticmethod
    def get_device_by_identifiers(device: dict) -> dict:
        """  query = {}
        if 'hid' in device:
            query.update({'hid': device['hid']})
        if 'pid' in device:
            query.update({'pid': device['pid']})
        if len(query) > 1:
            query = {'$or': query}
        return app.data.driver.db['devices'].find_one(query)
        """
        response = app.test_client().get('devices/' + device['hid'] + '?embedded=' + json.dumps({'components': 1}),
                                         content_type='application/json')
        data = json.loads(response.data)
        if response._status_code != 200:  # statusCode
            raise InnerRequestError(response._status_code, data)
        return data

    @staticmethod
    def get_parent(_id: objectid) -> dict or None:
        return app.data.driver.db['devices'].find_one({'components': {'$in': [_id]}})

    @staticmethod
    def seem_equal(x: dict, y: dict) -> bool:
        if id(x) == id(y):
            return True
        elif x['hid'] and y['hid'] and x['hid'] == y['hid']:
            return True
        elif 'pid' in x and 'pid' in y and x['pid'] == y['pid']:
            return True
            #  todo improve

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