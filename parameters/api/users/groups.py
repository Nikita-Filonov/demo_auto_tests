import uuid

from base.api.users.groups.group_checks import is_group_created, is_group_updated, is_group_deleted
from base.api.users.groups.groups import get_groups, get_group, create_group, update_group, delete_group, \
    get_groups_query
from models.users.group import Groups

group_id = uuid.uuid4()
group_payload = Groups

groups_methods = [
    {'method': get_groups, 'args': (), 'key': 'groups.get_groups'},
    {'method': get_group, 'args': (group_id,), 'key': 'groups.get_group'},
    {'method': create_group, 'args': (group_payload,), 'key': 'groups.create_group'},
    {'method': update_group, 'args': (group_id, group_payload), 'key': 'groups.update_group'},
    {'method': delete_group, 'args': (group_id,), 'key': 'groups.delete_group'},
    {'method': is_group_created, 'args': (group_id,), 'key': 'groups.is_group_created'},
    {'method': is_group_updated, 'args': (group_id,), 'key': 'groups.is_group_updated'},
    {'method': is_group_deleted, 'args': (group_id,), 'key': 'groups.is_group_deleted'},
    {'method': get_groups_query, 'args': ('?skip=0&take=10&requireTotalCount=true',), 'key': 'groups.get_groups_query'}
]
