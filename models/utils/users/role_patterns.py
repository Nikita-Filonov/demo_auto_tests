from models.users.activity import Activities
from models.users.group import Groups
from models.users.group_user import GroupUsers
from models.users.objective import Objectives
from models.users.objective_access import ObjectiveAccesses
from models.users.objective_records import ObjectiveRecords
from models.users.objective_workflow import ObjectiveWorkflows
from models.users.role_pattern import RolePatterns
from models.users.role_pattern_permission import RolePatternPermissions
from models.users.user import Users
from models.users.user_role import UserRoles
from models.utils.utils import filter_scopes

ROLE_PATTERN_SCOPE_TYPE = 'Group'

GROUP_OWNER_SCOPE = [
    *filter_scopes(Users.SCOPE, None, 'Read'),
    *filter_scopes(Groups.SCOPE, None, 'Read', 'Update'),
    *filter_scopes(GroupUsers.SCOPE, None, 'Read', 'Create', 'Delete'),
    *filter_scopes(UserRoles.SCOPE, None, 'Read', 'Create', 'Delete'),
]
GROUP_INSTRUCTOR_SCOPE = [
    *filter_scopes(Activities.SCOPE, None, 'Read'),
    *filter_scopes(Objectives.SCOPE, None, 'Read'),
    *filter_scopes(Groups.SCOPE, None, 'Read'),
    *filter_scopes(Users.SCOPE, None, 'Read'),
    *filter_scopes(GroupUsers.SCOPE, None, 'Read'),
    *filter_scopes(ObjectiveAccesses.SCOPE, None, 'Read'),
    *filter_scopes(ObjectiveRecords.SCOPE, None, 'Read'),
    *filter_scopes(ObjectiveWorkflows.SCOPE, None, 'Read', 'Update'),
]


def create_role_pattern(name, scopes, scope_type=ROLE_PATTERN_SCOPE_TYPE):
    """
    Can be used to create role pattern with gives list of scopes
    """
    role_pattern = RolePatterns.manager.create(scope_type=scope_type, name=name, as_json=False)
    exclude_scope_types = ['Activity.Read', 'Objective.Read', 'User.Read']

    for scope in scopes:
        safe_scope_type = None if scope['name'] in exclude_scope_types else scope_type
        RolePatternPermissions.manager.create(
            name=scope['name'],
            scope='{0}',
            scope_type=safe_scope_type,
            role_pattern_id=role_pattern.role_pattern_id.value,
            as_json=False
        )
