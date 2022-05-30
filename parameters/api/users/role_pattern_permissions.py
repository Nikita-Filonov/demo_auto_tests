import uuid

from base.api.users.role_pattern_permissions.role_pattern_permission_checks import is_role_pattern_permission_created, \
    is_role_pattern_permission_deleted
from base.api.users.role_pattern_permissions.role_pattern_permissions import get_role_pattern_permission, \
    get_role_pattern_permissions, create_role_pattern_permission, delete_role_pattern_permission, \
    get_role_pattern_permissions_query
from models.users.role_pattern_permission import RolePatternPermissions

role_pattern_permission_id = uuid.uuid4()
role_pattern_permission_payload = RolePatternPermissions

role_pattern_permission_methods = [
    {
        'method': get_role_pattern_permissions,
        'args': (),
        'key': 'role_pattern_permissions.get_role_pattern_permissions'
    },
    {
        'method': get_role_pattern_permission,
        'args': (role_pattern_permission_id,),
        'key': 'role_pattern_permissions.get_role_pattern_permission'
    },
    {
        'method': create_role_pattern_permission,
        'args': (role_pattern_permission_payload,),
        'key': 'role_pattern_permissions'
    },
    {
        'method': delete_role_pattern_permission,
        'args': (role_pattern_permission_id,),
        'key': 'role_pattern_permissions.create_role_pattern_permission'
    },
    {
        'method': is_role_pattern_permission_created,
        'args': (role_pattern_permission_id,),
        'key': 'role_pattern_permissions.is_role_pattern_permission_created'
    },
    {
        'method': is_role_pattern_permission_deleted,
        'args': (role_pattern_permission_id,),
        'key': 'role_pattern_permissions.is_role_pattern_permission_deleted'
    },
    {
        'method': get_role_pattern_permissions_query,
        'args': ('?skip=0&take=10&requireTotalCount=true',),
        'key': 'role_pattern_permissions.get_role_pattern_permissions_query'
    }
]
