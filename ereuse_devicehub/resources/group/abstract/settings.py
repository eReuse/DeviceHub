import copy

from ereuse_devicehub.resources.group.settings import Group, GroupSettings, children_groups


class Abstract(Group):
    children = copy.deepcopy(children_groups)
    children['schema']['data_relation'] = {
        'resource': 'packages',
        'field': 'label',
        'embeddable': True
    }


class AbstractSettings(GroupSettings):
    _schema = Abstract
    pass
