import pytest

from base.api.users.user_roles.user_roles import create_user_role
from models.users.user_role import UserRoles


@pytest.fixture(scope='function')
def user_role(request, user_function):
    payload = request.param if hasattr(request, 'param') else {}
    user_role_payload = {**UserRoles.manager.to_json, UserRoles.user_id.json: user_function['id']}
    return create_user_role({**user_role_payload, **payload}).json()
