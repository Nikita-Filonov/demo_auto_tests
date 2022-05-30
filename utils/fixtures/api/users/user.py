from typing import List, Tuple

import pytest

from base.api.identity.accounts import create_account
from base.api.users.roles.roles import get_roles
from base.api.users.user_roles.user_roles import create_user_role
from base.api.users.users.users import create_user_with_password, create_user
from models.identity.asp_net_user import AspNetUsers
from models.users.user import Users
from models.users.user_role import CreateUserRole
from models.utils.users.users import user_with_permissions


@pytest.fixture(scope='function')
def user_function():
    user_payload = Users.manager.to_json
    return create_user(user_payload).json()


@pytest.fixture(scope='class')
def user_class():
    user_payload = Users.manager.to_json
    return create_user(user_payload).json()


@pytest.fixture(scope='class')
def account_class():
    account_payload = AspNetUsers.manager.to_json
    return create_account(account_payload).json()


@pytest.fixture(scope='function')
def account_function():
    account_payload = AspNetUsers.manager.to_json
    return create_account(account_payload).json()


@pytest.fixture(scope='class')
def user_with_password_class(account_class):
    return create_user_with_password(account_class)


@pytest.fixture(scope='function')
def user_with_password_function(account_function):
    return create_user_with_password(account_function)


@pytest.fixture(scope='class')
def user_with_permissions_class(request, user_with_password_class):
    if not hasattr(request, 'param'):
        pytest.fail('Fixture "user_with_permissions_class" requires param')
    return user_with_permissions(request.param, user_with_password_class)


@pytest.fixture(scope='function')
def user_with_permissions_function(request, user_with_password_function):
    if not hasattr(request, 'param'):
        pytest.fail('Fixture "user_with_permissions_function" requires param')
    return user_with_permissions(request.param, user_with_password_function)


@pytest.fixture(scope='function')
def user_with_roles_function(request, user_with_password_function) -> Tuple[dict, List[dict]]:
    """
    Used to create user with password and given scope of roles

    Example:

        @pytest.mark.parametrize(
            'user_with_roles_function',
            [
                [SupportedRoles.AUTHOR, SupportedRoles.LEARNER],
                [SupportedRoles.AUTHOR, SupportedRoles.ADMINISTRATOR],
            ],
            indirect=['user_with_roles_function']
        )
        def test_some_user_roles(user_with_roles_function):
            user, roles = user_with_roles_function
            # where user is user object
            # where roles is list of roles objects which was assigned to the user
            ...
    """
    if not hasattr(request, 'param'):
        pytest.fail('Fixture "user_with_roles_class" requires param')

    safe_required_roles: List[str] = list(map(lambda r: r.value, request.param))

    roles: List[dict] = get_roles().json()
    required_roles: List[dict] = list(filter(lambda r: r['name'] in safe_required_roles, roles))

    for role in required_roles:
        payload = CreateUserRole(userId=user_with_password_function['id'], roleId=role['id'])
        create_user_role(payload.manager.to_json)

    return user_with_password_function, required_roles
