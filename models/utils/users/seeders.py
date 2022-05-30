from models.users.role_pattern import RolePatterns, SupportedRolePatterns
from models.utils.users.role_patterns import GROUP_INSTRUCTOR_SCOPE, GROUP_OWNER_SCOPE, create_role_pattern
from settings import DEFAULT_TENANT


def setup_role_patterns():
    """Setting up default role patterns. Needed to create group"""
    role_patterns = {
        SupportedRolePatterns.GROUP_INSTRUCTOR.value: GROUP_INSTRUCTOR_SCOPE,
        SupportedRolePatterns.GROUP_OWNER.value: GROUP_OWNER_SCOPE
    }
    for name, scope in role_patterns.items():
        # Checking if role patterns with "name" already exists
        is_role_pattern_exists = RolePatterns.manager.is_exists(
            name=name, tenant_id=DEFAULT_TENANT['id'], scope_type='Group')
        if not is_role_pattern_exists:
            create_role_pattern(name, scope)
