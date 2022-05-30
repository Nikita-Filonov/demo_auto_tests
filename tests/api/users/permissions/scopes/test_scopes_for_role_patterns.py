from http import HTTPStatus

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.role_patterns.role_patterns import get_role_patterns, get_role_pattern, create_role_pattern, \
    delete_role_pattern, update_role_pattern, get_role_patterns_query
from base.api.users.role_patterns.role_patterns_checks import is_role_patterns_created, is_role_patterns_deleted, \
    is_role_patterns_updated
from models.users.role_pattern import get_default_role_pattern, RolePatterns
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
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_ROLE_PATTERNS.value)
@pytest.mark.parametrize('user_with_permissions_class', [RolePatterns.SCOPE], indirect=['user_with_permissions_class'])
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForRolePatternsApi(BaseAPI):
    exclude = ['role_patterns', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    role_pattern_id = cache_callable(get_default_role_pattern)
    role_pattern_payload = RolePatterns

    @allure.id("1826")
    @allure.title('Check permissions for "RolePatterns" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_role_patterns, 'args': (), 'response': HTTPStatus.OK},
        {'method': get_role_pattern, 'args': (role_pattern_id,), 'response': HTTPStatus.OK},
        {'method': create_role_pattern, 'args': (role_pattern_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': update_role_pattern, 'args': (role_pattern_id, role_pattern_payload),
         'response': HTTPStatus.ACCEPTED},
        {'method': delete_role_pattern, 'args': (role_pattern_id,), 'response': HTTPStatus.ACCEPTED},
        {'method': is_role_patterns_created, 'args': (role_pattern_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_role_patterns_deleted, 'args': (role_pattern_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_role_patterns_updated, 'args': (role_pattern_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': get_role_patterns_query, 'args': ('?skip=0&take=10&requireTotalCount=true',),
         'response': HTTPStatus.OK},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_role_patterns_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
