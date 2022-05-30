import pytest

from base.api.users.group_users.group_users import create_group_user
from models.users.group_user import GroupUsers


@pytest.fixture(scope='function')
def group_user_function():
    group_user_payload = GroupUsers.manager.to_json
    return create_group_user(group_user_payload).json()


@pytest.fixture(scope='function')
def group_user_class():
    group_user_payload = GroupUsers.manager.to_json
    return create_group_user(group_user_payload).json()
