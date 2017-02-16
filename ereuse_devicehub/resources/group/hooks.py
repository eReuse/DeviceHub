from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.resources.group.settings import Group
from ereuse_devicehub.utils import Naming


def set_children(_, groups: list):
    for group in groups:
        if group.get('@type', None) in Group.types:
            domain = GroupDomain.children_resources[Naming.resource(group['@type'])]
            domain.update_children({}, group['children'], group['ancestors'], group['label'])


def update_children(_, updated: dict, original: dict):
    if updated.get('@type', None) in Group.types:
        domain = GroupDomain.children_resources[Naming.resource(original['@type'])]
        domain.update_children(original['children'], updated['children'], original['ancestors'], original['label'])


def delete_children(_, group):
    if group.get('@type', None) in Group.types:
        domain = GroupDomain.children_resources[Naming.resource(group['@type'])]
        domain.update_children(group['children'], {}, group['ancestors'], group['label'])
