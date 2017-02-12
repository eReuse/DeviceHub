from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.resources.group.settings import Group


def set_children(_, groups: list):
    for group in groups:
        if group.get('@type', None) in Group.resource_types:
            domain = GroupDomain.children_resources[group['@type']]
            domain.update_children({}, group['children'], group['ancestors'], group['label'])


def update_children(_, updated: dict, original: dict):
    if updated.get('@type', None) in Group.resource_types:
        domain = GroupDomain.children_resources[original['@type']]
        domain.update_children(original['children'], updated['children'], original['ancestors'], original['label'])


def delete_children(_, group):
    if group.get('@type', None) in Group.resource_types:
        domain = GroupDomain.children_resources[group['@type']]
        domain.update_children(group['children'], {}, group['ancestors'], group['label'])
