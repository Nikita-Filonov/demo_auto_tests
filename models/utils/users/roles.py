from models.users.activity import Activities
from models.users.group import Groups
from models.users.group_user import GroupUsers
from models.users.oauth1_credentials import Oauth1Credentials
from models.users.objective import Objectives
from models.users.objective_access import ObjectiveAccesses
from models.users.objective_records import ObjectiveRecords
from models.users.objective_workflow import ObjectiveWorkflows
from models.users.objective_workflow_aggregate import ObjectiveWorkflowAggregates
from models.users.permission import Permissions
from models.users.role import Roles, RolePermissions
from models.users.role_pattern import RolePatterns
from models.users.role_pattern_permission import RolePatternPermissions
from models.users.tenant import Tenants
from models.users.user import Users
from models.users.user_role import UserRoles
from models.utils.utils import filter_scopes
from settings import DEFAULT_USER

LEARNER_SCOPE = [
    *filter_scopes(Objectives.SCOPE, 'Self', 'Read'),
    *filter_scopes(Users.SCOPE, 'Self', 'Read'),
    *filter_scopes(ObjectiveAccesses.SCOPE, 'Self', 'Read'),
    *filter_scopes(ObjectiveWorkflowAggregates.SCOPE, 'Self', 'Read', 'Update'),
    *filter_scopes(ObjectiveRecords.SCOPE, 'Self', 'Read', 'Create'),
    *filter_scopes(ObjectiveWorkflows.SCOPE, 'Self', 'Read', 'Create', 'Update')
]
INSTRUCTOR_SCOPE = [
    *filter_scopes(ObjectiveAccesses.SCOPE, None, 'Update', 'Create'),
    *filter_scopes(Activities.SCOPE, None, 'Read', 'Update'),
    *filter_scopes(Objectives.SCOPE, None, 'Read', 'Update'),
    *filter_scopes(ObjectiveAccesses.SCOPE, None, 'Read'),
    *filter_scopes(ObjectiveRecords.SCOPE, None, 'Read'),
    *filter_scopes(ObjectiveWorkflows.SCOPE, None, 'Read'),
    *filter_scopes(ObjectiveWorkflowAggregates.SCOPE, None, 'Delete', 'Update', 'Create'),
]
AUTHOR_SCOPE = [
    *filter_scopes(Activities.SCOPE, None, 'Read', 'Update', 'Create'),
    *filter_scopes(Objectives.SCOPE, None, 'Read', 'Update', 'Create'),
]
ADMINISTRATOR_SCOPE = [
    *Activities.SCOPE,
    *Groups.SCOPE,
    *GroupUsers.SCOPE,
    *Oauth1Credentials.SCOPE,
    *Objectives.SCOPE,
    *ObjectiveAccesses.SCOPE,
    *ObjectiveRecords.SCOPE,
    *ObjectiveWorkflows.SCOPE,
    *ObjectiveWorkflowAggregates.SCOPE,
    *Permissions.SCOPE,
    *Roles.SCOPE,
    *RolePatterns.SCOPE,
    *RolePatternPermissions.SCOPE,
    *Users.SCOPE,
    *UserRoles.SCOPE
]
TENANT_ADMIN_SCOPE = Tenants.SCOPE


def create_role(name, scopes, user_id=DEFAULT_USER['id']):
    """
    :param user_id:
    :param name:
    :param scopes:
    :return:
    """
    role_id = Roles.manager.create(name=name, as_json=False).role_id.value

    permissions = []
    # for each scope in permission
    for scope in scopes:
        # we creating permission instance
        permission = Permissions.manager.get_or_create(
            name=scope['name'],
            scope=scope['scope'],
            scope_type=scope['scopeType'],
            as_json=False
        )
        permissions.append(permission)

    # for each permission
    for permission in permissions:
        # we creating many to many relation
        # for more info look at models.role.RolePermission model
        RolePermissions.manager.create(role_id=role_id, permission_id=permission.permission_id.value)

    UserRoles.manager.create(role_id=role_id, user_id=user_id)
