from base.api.base import BaseAPI
from models.users.group import Groups
from models.users.role_pattern_permission import RolePatternPermissions


class GroupsBaseAPI(BaseAPI):
    """Wrapper around ``BaseAPI`` that have specific values for groups autotests"""
    group = Groups.manager
    scope_keys = [
        RolePatternPermissions.name.json,
        RolePatternPermissions.scope.json,
        RolePatternPermissions.scope_type.json
    ]
    group_keys = [Groups.group_id.json, Groups.name.json]
