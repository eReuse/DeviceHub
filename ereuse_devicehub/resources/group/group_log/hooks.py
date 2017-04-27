from pydash import difference
from pydash import is_empty
from pydash import map_values
from pydash import omit
from pydash import pick

from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.resources.group.group_log.settings import UpdateGroupLogEntry, GroupLogEntry
from ereuse_devicehub.resources.group.settings import Group
from ereuse_devicehub.rest import execute_post_internal


def add_group_change_to_log(_, updated: dict, original: dict):
    if updated.get('@type', None) in Group.types:
        RESOURCES = GroupDomain.children_resources
        orig = original.get('children', {})
        upd = updated.get('children', {})
        entry = {
            '@type': UpdateGroupLogEntry.type_name,
            'parent': pick(original if '@type' in original else updated, '@type', 'label'),
            # Compute the difference between updated and original, removing empty '[]'
            'added': omit(map_values(RESOURCES, lambda _, t: difference(upd.get(t, []), orig.get(t, []))), is_empty),
            'removed': omit(map_values(RESOURCES, lambda _, t: difference(orig.get(t, []), upd.get(t, []))), is_empty)
        }
        # We want to generate _created
        execute_post_internal(GroupLogEntry.resource_name, entry, skip_validation=True)


def set_children(_, groups: list):
    for group in groups:
        add_group_change_to_log(_, group, {})


def delete_children(_, group: dict):
    add_group_change_to_log(_, {}, group)
