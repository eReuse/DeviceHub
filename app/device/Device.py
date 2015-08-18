from DeviceWare import app
from app.device.exceptions import HidError

__author__ = 'Xavier Bustamante Talavera'


class Device:
    @staticmethod
    def compute_hid(device: dict) -> int:
        if not device['manufacturer']:
            raise HidError('Device manufacturer doesn\'t exist.')
        if not device['serialNumber']:
            raise HidError('Device serialNumber doesn\'t exist.')
        device['hid'] = device['manufacturer'] + device['serialNumber']
        return device['hid']

    @staticmethod
    def get_device_by_identifiers(device: dict) -> dict:
        query = {}
        if device['hid']:
            query.update({'hid': device['hid']})
        if device['pid']:
            query.update({'pid': device['pid']})
        if len(query) > 1:
            query = {'$or': query}
        return app.data.driver.db['devices'].find_one(query)

    @staticmethod
    def get_parent(_id: 'objectid') -> dict or None:
        return app.data.driver.db['devices'].find_one({'components': [_id]})

    @staticmethod
    def seem_equal(x: dict, y: dict) -> bool:
        if id(x) == id(y): return True
        elif x['hid'] and y['hid'] and x['hid'] == y['hid']: return True
        elif x['pid'] and y['pid'] and x['pid'] == y['pid']: return True
        #  todo improve
