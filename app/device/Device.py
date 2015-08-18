from DeviceWare import app

__author__ = 'Xavier Bustamante Talavera'


class Device:
    @staticmethod
    def compute_hid(device: dict) -> int:
        if not device['manufacturer']:
            raise HidError('Cannot compute hid: device manufacturer doesn\'t exist.')
        if not device['serialNumber']:
            raise HidError('Cannot compute hid: device serialNumber doesn\'t exist.')
        device['hid'] = device['manufacturer'] + device['serialNumber']
        return device['hid']

    @staticmethod
    def get_device_by_identifiers(hid: str='', pid: str=''):
        devices = app.data.driver.db['devices']
        query = {'$or': [{'hid': hid}, {'pid': pid}]}
        return devices.find_one(query)

    @staticmethod
    def get_parent(_id: 'objectid') -> dict or None:
        devices = app.data.driver.db['devices']
        return devices.find_one({'components': [_id]})