import pytest

from base.api.users.groups.groups import create_group
from base.api.users.user_roles.user_roles import create_user_role
from models.users.group import Groups
from models.users.role_pattern import SupportedRolePatterns
from models.users.user_role import UserRoles


@pytest.fixture(scope='function')
def group_function():
    group_payload = Groups.manager.to_json
    return create_group(group_payload).json()


@pytest.fixture(scope='function')
def group_class():
    group_payload = Groups.manager.to_json
    return create_group(group_payload).json()


@pytest.fixture(scope='function')
def group_owner(group_user_function, user_with_password_function):
    role_name = SupportedRolePatterns.get_owner_role(group_user_function['group']['id'])
    owner_payload = {UserRoles.user_id.json: user_with_password_function['id'], 'roleName': role_name}

    owner_role = create_user_role(owner_payload).json()

    return {
        'owner': user_with_password_function,
        'owner_role': owner_role,
        'group': group_user_function['group'],
        'user': group_user_function['user']
    }


@pytest.fixture(scope='function')
def group_instructor(group_user_function, user_with_password_function):
    role_name = SupportedRolePatterns.get_instructor_role(group_user_function['group']['id'])
    instructor_payload = {UserRoles.user_id.json: user_with_password_function['id'], 'roleName': role_name}

    instructor_role = create_user_role(instructor_payload).json()

    return {
        'instructor': user_with_password_function,
        'instructor_role': instructor_role,
        'group': group_user_function['group']
    }


@pytest.fixture(scope='function')
def group_instructor_without_user(group_function, user_with_password_function):
    role_name = SupportedRolePatterns.get_instructor_role(group_function['id'])
    instructor_payload = {UserRoles.user_id.json: user_with_password_function['id'], 'roleName': role_name}

    instructor_role = create_user_role(instructor_payload).json()

    return {
        'instructor': user_with_password_function,
        'instructor_role': instructor_role,
        'group': group_function
    }
