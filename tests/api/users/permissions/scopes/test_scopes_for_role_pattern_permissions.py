from http import HTTPStatus

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.role_pattern_permissions.role_pattern_permission_checks import is_role_pattern_permission_created, \
    is_role_pattern_permission_deleted
from base.api.users.role_pattern_permissions.role_pattern_permissions import get_role_pattern_permissions, \
    get_role_pattern_permission, create_role_pattern_permission, delete_role_pattern_permission, \
    get_role_pattern_permissions_query
from models.users.role_pattern_permission import get_default_role_pattern_permission, RolePatternPermissions
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
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_ROLE_PATTERN_PERMISSIONS.value)
@pytest.mark.parametrize(
    'user_with_permissions_class',
    [RolePatternPermissions.SCOPE],
    indirect=['user_with_permissions_class']
)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForRolePatternPermissionsApi(BaseAPI):
    exclude = ['role_pattern_permissions', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    role_pattern_permission_id = cache_callable(get_default_role_pattern_permission)
    role_pattern_permission_payload = RolePatternPermissions

    @allure.id("1825")
    @allure.title('Check permissions for "RolePatternPermissions" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_role_pattern_permissions, 'args': (), 'response': HTTPStatus.OK},
        {'method': get_role_pattern_permission, 'args': (role_pattern_permission_id,), 'response': HTTPStatus.OK},
        {'method': create_role_pattern_permission, 'args': (role_pattern_permission_payload,),
         'response': HTTPStatus.ACCEPTED},
        {'method': delete_role_pattern_permission, 'args': (role_pattern_permission_id,),
         'response': HTTPStatus.ACCEPTED},
        {'method': is_role_pattern_permission_created, 'args': (role_pattern_permission_id,),
         'response': HTTPStatus.NOT_FOUND},
        {'method': is_role_pattern_permission_deleted, 'args': (role_pattern_permission_id,),
         'response': HTTPStatus.NOT_FOUND},
        {'method': get_role_pattern_permissions_query, 'args': ('?skip=0&take=10&requireTotalCount=true',),
         'response': HTTPStatus.OK},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_role_pattern_permissions_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
