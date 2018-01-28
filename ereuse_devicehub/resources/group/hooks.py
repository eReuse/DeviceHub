from flask import current_app

from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.resources.group.settings import Group
from ereuse_utils.naming import Naming


def set_children(_, groups: list):
    """Sets children and permissions when POSTing a group."""
    for group in groups:
        if group.get('@type', None) in Group.types:
            domain = GroupDomain.children_resources[Naming.resource(group['@type'])]
            domain.update_children({}, group['children'], group['ancestors'], group['_id'], group['perms'])


def update_children(_, updated: dict, original: dict):
    """Updates children and permissions when modifying the ``children`` property in the group."""
    # todo what happens when I patch *children* and *perms*?
    if updated.get('@type', None) in Group.types and updated.get('children', None) is not None:
        domain = GroupDomain.children_resources[Naming.resource(original['@type'])]
        domain.update_children(original['children'], updated['children'], original['ancestors'], original['_id'],
                               original['perms'])


def delete_children(_, group):
    """Removes children from the group and removes their inherited permissions."""
    if group.get('@type', None) in Group.types:
        domain = GroupDomain.children_resources[Naming.resource(group['@type'])]
        domain.update_children(group['children'], {}, group['ancestors'], group['_id'], group['perms'])


def set_short_id(_, groups: list):
    """Assigns an id to a group when POSTing it."""
    for group in groups:
        if group.get('@type', None) in Group.types:
            group['_id'] = current_app.sid.generate()


def update_perms(_, updated: dict, original: dict):
    """Update permissions for groups when PATCHing the ``perms`` property of the group."""
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
