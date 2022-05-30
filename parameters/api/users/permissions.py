import uuid

from base.api.users.permissions.permission_checks import is_permission_created, is_permission_updated
from base.api.users.permissions.permissions import get_permissions, get_permission, get_permissions_query, \
    create_permission, update_permission
from models.users.permission import Permissions

permission_id = uuid.uuid4()
permission_payload = Permissions

permissions_methods = [
    {'method': get_permissions, 'args': (), 'key': 'permissions.get_permissions'},
    {'method': get_permission, 'args': (permission_id,), 'key': 'permissions.get_permission'},
    {'method': get_permissions_query, 'args': ('?skip=0&take=10&requireTotalCount=true',),
     'key': 'permissions.get_permissions_query'},
    {'method': create_permission, 'args': (permission_payload,), 'key': 'permissions.create_permission'},
    {'method': update_permission, 'args': (permission_id, permission_payload), 'key': 'permissions.update_permission'},
    {'method': is_permission_created, 'args': (permission_id,), 'key': 'permissions.is_permission_created'},
    {'method': is_permission_updated, 'args': (permission_id,), 'key': 'permissions.is_permission_updated'}
]
