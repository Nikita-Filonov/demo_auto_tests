import uuid

from base.api.users.user_roles.user_roles import get_user_role, get_user_roles, get_user_role_query, create_user_role, \
    delete_user_role
from base.api.users.user_roles.user_roles_checks import is_user_role_created, is_user_role_deleted
from models.users.user_role import UserRoles

user_role_id = uuid.uuid4()
user_role_payload = UserRoles

user_role_methods = [
    {'method': get_user_role, 'args': (user_role_id,), 'key': 'user_roles.get_user_role'},
    {'method': get_user_roles, 'args': (), 'key': 'user_roles.get_user_roles'},
    {'method': get_user_role_query, 'args': ('?skip=0&take=10&requireTotalCount=true',),
     'key': 'user_roles.get_user_role_query'},
    {'method': create_user_role, 'args': (user_role_payload,), 'key': 'user_roles.create_user_role'},
    {'method': delete_user_role, 'args': (user_role_id,), 'key': 'user_roles.delete_user_role'},
    {'method': is_user_role_created, 'args': (user_role_id,), 'key': 'user_roles.is_user_role_created'},
    {'method': is_user_role_deleted, 'args': (user_role_id,), 'key': 'user_roles.is_user_role_deleted'}
]
