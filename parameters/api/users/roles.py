import uuid

from base.api.users.roles.role_checks import is_role_created, is_role_updated
from base.api.users.roles.roles import get_roles, get_role, get_roles_query, create_role, update_role
from models.users.role import Roles

role_id = uuid.uuid4()
role_payload = Roles

roles_methods = [
    {'method': get_roles, 'args': (), 'key': 'roles.get_roles'},
    {'method': get_role, 'args': (role_id,), 'key': 'roles.get_role'},
    {'method': get_roles_query, 'args': ('?skip=0&take=10&requireTotalCount=true',), 'key': 'roles.get_roles_query'},
    {'method': create_role, 'args': (role_payload,), 'key': 'roles.create_role'},
    {'method': update_role, 'args': (role_id, role_payload), 'key': 'roles.update_role'},
    {'method': is_role_created, 'args': (role_id,), 'key': 'roles.is_role_created'},
    {'method': is_role_updated, 'args': (role_id,), 'key': 'roles.is_role_updated'}
]
