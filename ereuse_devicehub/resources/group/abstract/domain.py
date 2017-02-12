from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.group.abstract.settings import AbstractSettings
from ereuse_devicehub.resources.group.domain import GroupDomain


class AbstractDomain(GroupDomain):
    resource_settings = AbstractSettings
    foreign_key_in_device = None

    @classmethod
    def device_set_group(cls, device_id, group_id: str):
        # We add the group at the end of the device
        update_dict = {'$push': {cls.foreign_key_in_device: {'$each': [group_id], '$position': 0}}}
        DeviceDomain.update_one_raw({'_id': device_id}, update_dict)

    @classmethod
    def device_unset_group(cls, device_id: str):
        DeviceDomain.update_one_raw({'_id': device_id}, {'$pull': {cls.foreign_key_in_device: ''}})
