import uuid

from base.api.users.group_users.group_user_checks import is_group_user_created, is_group_user_deleted
from base.api.users.group_users.group_users import get_group_users, get_group_user, create_group_user, \
    delete_group_user, get_group_users_query
from models.users.group_user import GroupUsers

group_user_id = uuid.uuid4()
group_user_payload = GroupUsers

group_user_methods = [
    {'method': get_group_users, 'args': (), 'key': 'group_users.get_group_users'},
    {'method': get_group_user, 'args': (group_user_id,), 'key': 'group_users.get_group_user'},
    {'method': create_group_user, 'args': (group_user_payload,), 'key': 'group_users.create_group_user'},
    {'method': delete_group_user, 'args': (group_user_id,), 'key': 'group_users.delete_group_user'},
    {'method': is_group_user_created, 'args': (group_user_id,), 'key': 'group_users.is_group_user_created'},
    {'method': is_group_user_deleted, 'args': (group_user_id,), 'key': 'group_users.is_group_user_deleted'},
    {'method': get_group_users_query, 'args': ('?skip=0&take=10&requireTotalCount=true',),
     'key': 'group_users.get_group_users_query'}
]
