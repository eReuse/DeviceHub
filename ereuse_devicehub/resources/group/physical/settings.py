from ereuse_devicehub.resources.group.settings import Group, GroupSettings


class Physical(Group):
    pass


class PhysicalSettings(GroupSettings):
    _schema = Physical
    pass
