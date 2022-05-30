from http import HTTPStatus

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.roles.role_checks import is_role_created, is_role_updated
from base.api.users.roles.roles import get_roles, get_role, get_roles_query, create_role, update_role
from models.users.role import Roles, get_default_role
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
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_ROLES.value)
@pytest.mark.parametrize('user_with_permissions_class', [Roles.SCOPE], indirect=['user_with_permissions_class'])
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForRolesApi(BaseAPI):
    exclude = ['roles', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    role_id = cache_callable(get_default_role)
    role_payload = Roles

    @allure.id("1822")
    @allure.title('Check permissions for "Roles" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_roles, 'args': (), 'response': HTTPStatus.OK},
        {'method': get_role, 'args': (role_id,), 'response': HTTPStatus.OK},
        {'method': get_roles_query, 'args': ('?skip=0&take=10&requireTotalCount=true',), 'response': HTTPStatus.OK},
        {'method': create_role, 'args': (role_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': update_role, 'args': (role_id, role_payload), 'response': HTTPStatus.ACCEPTED},
        {'method': is_role_created, 'args': (role_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_role_updated, 'args': (role_id,), 'response': HTTPStatus.NOT_FOUND},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_roles_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
