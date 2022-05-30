from http import HTTPStatus

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.user_roles.user_roles import get_user_role, get_user_roles, get_user_role_query, create_user_role, \
    delete_user_role
from base.api.users.user_roles.user_roles_checks import is_user_role_created, is_user_role_deleted
from models.users.user_role import get_default_user_role, UserRoles
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.api.users.permissions import PermissionsStory
from utils.api.users.common import Endpoint
from utils.api.users.permissions import make_methods_payload_for_permissions, EXCLUDE_PERMISSIONS_ENDPOINTS, \
    check_permissions_for_entity
from utils.formatters.parametrization import to_method_param
from utils.utils import cache_callable


@pytest.mark.api
@pytest.mark.permissions
@pytest.mark.permissions_scopes
@allure.epic('Core LMS')
@allure.feature('Permissions')
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_USER_ROLES.value)
@pytest.mark.parametrize('user_with_permissions_class', [UserRoles.SCOPE], indirect=['user_with_permissions_class'])
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForUserRolesApi(BaseAPI):
    exclude = ['user_roles', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    user_role_id = cache_callable(get_default_user_role)
    user_role_payload = UserRoles

    @allure.id("1821")
    @allure.title('Check permissions for "UserRoles" model (API)')
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-606',
        name='User with permissions for "UserRoles" has access to "Roles"'
    )
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1577', name='Problem when creating user role')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_user_role, 'args': (user_role_id,), 'response': HTTPStatus.OK},
        {'method': get_user_roles, 'args': (), 'response': HTTPStatus.OK},
        {'method': get_user_role_query, 'args': ('?skip=0&take=10&requireTotalCount=true',), 'response': HTTPStatus.OK},
        {'method': create_user_role, 'args': (user_role_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': delete_user_role, 'args': (user_role_id,), 'response': HTTPStatus.ACCEPTED},
        {'method': is_user_role_created, 'args': (user_role_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_user_role_deleted, 'args': (user_role_id,), 'response': HTTPStatus.NOT_FOUND},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_user_roles_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
