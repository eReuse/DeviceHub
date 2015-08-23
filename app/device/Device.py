from bson import objectid
from app.app import app
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
        query = {}
        if 'hid' in device:
            query.update({'hid': device['hid']})
        if 'pid' in device:
            query.update({'pid': device['pid']})
        if len(query) > 1:
            query = {'$or': query}
        return app.data.driver.db['devices'].find_one(query)

    @staticmethod
    def get_parent(_id: objectid) -> dict or None:
        return app.data.driver.db['devices'].find_one({'components': [_id]})

    @staticmethod
    def seem_equal(x: dict, y: dict) -> bool:
        if id(x) == id(y):
            return True
        elif x['hid'] and y['hid'] and x['hid'] == y['hid']:
            return True
        elif x['pid'] and y['pid'] and x['pid'] == y['pid']:
            return True
        #  todo improve
