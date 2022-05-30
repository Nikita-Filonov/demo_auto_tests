from models_manager import Q

from models.users.activity import Activities, CreateActivities, UpdateActivities
from models.users.grades import Grades
from models.users.grading_scale import GradingScales
from models.users.group import Groups, CreateGroups, UpdateGroups, DeleteGroups
from models.users.group_user import GroupUsers, CreateGroupUsers, DeleteGroupUsers
from models.users.lms_user import UserExtensions
from models.users.mail_message import MailMessages
from models.users.oauth1_credentials import Oauth1Credentials, CreateOauth1Credentials, UpdateOauth1Credentials
from models.users.objective import Objectives, CreateObjectives, UpdateObjectives
from models.users.objective_access import ObjectiveAccesses, CreateObjectiveAccesses, DeleteObjectiveAccesses
from models.users.objective_records import ObjectiveRecords
from models.users.objective_workflow import ObjectiveWorkflows
from models.users.objective_workflow_aggregate import ObjectiveWorkflowAggregates
from models.users.permission import Permissions
from models.users.resource_libraries import CreateResourceLibraries, UpdateResourceLibraries, \
    DeleteResourceLibraries, ResourceLibraries
from models.users.role import Roles, SupportedRoles, CreateRoles, UpdateRoles, DeleteRoles
from models.users.role_pattern import RolePatterns, SupportedRolePatterns, CreateRolePatterns, UpdateRolePatterns, \
    DeleteRolePatterns
from models.users.role_pattern_permission import RolePatternPermissions, CreateRolePatternPermissions, \
    DeleteRolePatternPermissions
from models.users.tenant import Tenants
from models.users.tenant_setting import TenantSettings, SupportedSettings
from models.users.user import Users, CreateUsers, UpdateUsers
from models.users.user_role import UserRoles, CreateUserRoles, DeleteUserRoles
from models.utils.users.tenants import get_safe_tenants
from models.utils.utils import clear_log
from settings import DEFAULT_TENANT, DEFAULT_USER

TENANT_QUERY = {'tenant_id': DEFAULT_TENANT['id'], 'as_json': False}


def clear_groups():
    """Clears groups and all related models"""
    with clear_log(GroupUsers):
        GroupUsers.manager.filter(**TENANT_QUERY).delete()
        CreateGroupUsers.manager.filter(**TENANT_QUERY).delete()
        DeleteGroupUsers.manager.filter(**TENANT_QUERY).delete()

    with clear_log(Groups):
        Groups.manager.filter(**TENANT_QUERY).delete()
        CreateGroups.manager.filter(**TENANT_QUERY).delete()
        UpdateGroups.manager.filter(**TENANT_QUERY).delete()
        DeleteGroups.manager.filter(**TENANT_QUERY).delete()


def clear_resource_libraries():
    """Clears resource libraries and all related models"""
    with clear_log(ResourceLibraries):
        ResourceLibraries.manager.filter(**TENANT_QUERY).delete()
        CreateResourceLibraries.manager.filter(**TENANT_QUERY).delete()
        UpdateResourceLibraries.manager.filter(**TENANT_QUERY).delete()
        DeleteResourceLibraries.manager.filter(**TENANT_QUERY).delete()


def clear_activities():
    """Clears activities and all related models"""
    with clear_log(Activities):
        Activities.manager.filter(**TENANT_QUERY).delete()
        CreateActivities.manager.filter(**TENANT_QUERY).delete()
        UpdateActivities.manager.filter(**TENANT_QUERY).delete()


def clear_objectives():
    """Clears objectives and all related models"""
    with clear_log(ObjectiveWorkflowAggregates):
        ObjectiveWorkflowAggregates.manager.filter(**TENANT_QUERY).delete()

    with clear_log(ObjectiveWorkflows):
        ObjectiveWorkflows.manager.filter(**TENANT_QUERY).update(objective_record_id=None)

    with clear_log(ObjectiveRecords):
        ObjectiveRecords.manager.filter(**TENANT_QUERY).delete()

    with clear_log(ObjectiveWorkflows):
        ObjectiveWorkflows.manager.filter(**TENANT_QUERY).delete()

    with clear_log(ObjectiveAccesses):
        ObjectiveAccesses.manager.filter(**TENANT_QUERY).delete()
        CreateObjectiveAccesses.manager.filter(**TENANT_QUERY).delete()
        DeleteObjectiveAccesses.manager.filter(**TENANT_QUERY).delete()

    with clear_log(Objectives):
        Objectives.manager.filter(**TENANT_QUERY).delete()
        CreateObjectives.manager.filter(**TENANT_QUERY).delete()
        UpdateObjectives.manager.filter(**TENANT_QUERY).delete()


def clear_oauth1_credentials():
    """Clears oauth1 credentials and all related models"""
    with clear_log(Oauth1Credentials):
        Oauth1Credentials.manager.filter(**TENANT_QUERY).delete()
        CreateOauth1Credentials.manager.filter(**TENANT_QUERY).delete()
        UpdateOauth1Credentials.manager.filter(**TENANT_QUERY).delete()


def clear_users():
    """Clears users and all related models"""
    default_roles = SupportedRoles.to_list()
    safe_tenants = get_safe_tenants(extra_tenants=[DEFAULT_TENANT['id']])

    tenant_users = Users.manager.filter(Q(tenant_id__in=safe_tenants) & Q(user_id__not_equal=DEFAULT_USER['id']))
    safe_users = tuple(user['user_id'] for user in tenant_users)

    tenant_roles = Roles.manager.filter(Q(name__not_in=default_roles) & Q(tenant_id__in=safe_tenants))
    safe_roles = tuple(role['role_id'] for role in tenant_roles)

    with clear_log(UserRoles):
        UserRoles.manager.filter(role_id__in=safe_roles, as_json=False).delete()
        CreateUserRoles.manager.filter(**TENANT_QUERY).delete()
        DeleteUserRoles.manager.filter(**TENANT_QUERY).delete()

    with clear_log(Roles):
        Roles.manager.filter(role_id__in=safe_roles, as_json=False).delete()
        CreateRoles.manager.filter(**TENANT_QUERY).delete()
        UpdateRoles.manager.filter(**TENANT_QUERY).delete()
        DeleteRoles.manager.filter(**TENANT_QUERY).delete()

    with clear_log(UserExtensions):
        UserExtensions.manager.filter(tenant_id=DEFAULT_TENANT['id'], as_json=False).delete()

    with clear_log(Users):
        Users.manager.filter(user_id__in=safe_users, as_json=False).delete()
        CreateUsers.manager.filter(**TENANT_QUERY).delete()
        UpdateUsers.manager.filter(**TENANT_QUERY).delete()

    with clear_log(MailMessages):
        MailMessages.manager.filter(tenant_id=DEFAULT_TENANT['id'], as_json=False).delete()


def clear_role_patterns():
    """Clears role patterns and all related models"""
    safe_tenants = get_safe_tenants(extra_tenants=[DEFAULT_TENANT['id']])
    default_role_patterns = [SupportedRolePatterns.GROUP_OWNER.value, SupportedRolePatterns.GROUP_INSTRUCTOR.value]
    tenant_role_patterns = RolePatterns.manager.filter(name__not_in=default_role_patterns, tenant_id__in=safe_tenants)
    safe_role_patterns = tuple(role_pattern['role_pattern_id'] for role_pattern in tenant_role_patterns)

    with clear_log(RolePatternPermissions):
        RolePatternPermissions.manager.filter(role_pattern_id__in=safe_role_patterns, as_json=False).delete()
        CreateRolePatternPermissions.manager.filter(**TENANT_QUERY).delete()
        DeleteRolePatternPermissions.manager.filter(**TENANT_QUERY).delete()

    with clear_log(RolePatterns):
        RolePatterns.manager.filter(role_pattern_id__in=safe_role_patterns, as_json=False).delete()
        CreateRolePatterns.manager.filter(**TENANT_QUERY).delete()
        UpdateRolePatterns.manager.filter(**TENANT_QUERY).delete()
        DeleteRolePatterns.manager.filter(**TENANT_QUERY).delete()


def clear_tenants():
    """Clears tenants and all related models"""
    safe_tenants = get_safe_tenants()

    with clear_log(Permissions):
        Permissions.manager.filter(tenant_id__in=safe_tenants, as_json=False).delete()

    with clear_log(Tenants):
        Tenants.manager.filter(tenant_id__in=safe_tenants, as_json=False).delete()

    with clear_log(TenantSettings):
        tenants_for_settings = (*safe_tenants, DEFAULT_TENANT['id'])
        default_settings = tuple(SupportedSettings.to_list())
        TenantSettings.manager.filter(
            tenant_id__in=tenants_for_settings, name__not_in=default_settings, as_json=False).delete()


def clear_grading_scales():
    """Clears grading scales and all related models"""
    safe_tenants = get_safe_tenants(extra_tenants=[DEFAULT_TENANT['id']])

    with clear_log(Grades):
        Grades.manager.filter(tenant_id__in=safe_tenants, as_json=False).delete()

    with clear_log(GradingScales):
        GradingScales.manager.filter(tenant_id__in=safe_tenants, as_json=False).delete()


if __name__ == '__main__':
    clear_groups()
    clear_objectives()
    clear_activities()
    clear_oauth1_credentials()
    clear_users()
    clear_role_patterns()
    clear_tenants()
    clear_resource_libraries()
    clear_grading_scales()
