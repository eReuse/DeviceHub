import copy

from ereuse_devicehub.resources.group.settings import Group, GroupSettings


class Abstract(Group):
    pass

class AbstractSettings(GroupSettings):
    _schema = Abstract
    pass
