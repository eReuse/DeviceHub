from flask import current_app

from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.resources.group.settings import Group
from ereuse_devicehub.utils import Naming


def set_children(_, groups: list):
    for group in groups:
        if group.get('@type', None) in Group.types:
            domain = GroupDomain.children_resources[Naming.resource(group['@type'])]
            domain.update_children({}, group['children'], group['ancestors'], group['_id'], group['perms'])


def update_children(_, updated: dict, original: dict):
    if updated.get('@type', None) in Group.types and updated.get('children', None) is not None:
        domain = GroupDomain.children_resources[Naming.resource(original['@type'])]
        domain.update_children(original['children'], updated['children'], original['ancestors'], original['_id'],
                               original['perms'])


def delete_children(_, group):
    if group.get('@type', None) in Group.types:
        domain = GroupDomain.children_resources[Naming.resource(group['@type'])]
        domain.update_children(group['children'], {}, group['ancestors'], group['_id'], group['perms'])


def set_short_id(_, groups: list):
    for group in groups:
        if group.get('@type', None) in Group.types:
            group['_id'] = current_app.sid.generate()


def update_perms(_, updated: dict, original: dict):
    """Update permissions for groups when PATCHing"""
    if updated.get('@type', None) in Group.types and updated.get('perms', None) is not None:
        domain = GroupDomain.children_resources[Naming.resource(original['@type'])]
        updated['sharedWith'] = domain.update_and_inherit_perms(original['_id'], original['@type'],
                                                                original.get('label', None),
                                                                set(original['sharedWith']), original['perms'],
                                                                updated['perms'])


def set_perms(_, groups: list):
    """Set permissions for groups when POSTing"""
    for g in groups:
        if g.get('@type', None) in Group.types:
            domain = GroupDomain.children_resources[Naming.resource(g['@type'])]
            g['sharedWith'] = domain.update_and_inherit_perms(g['_id'], g['@type'], g.get('label', None),
                                                              set(), [], g['perms'])
