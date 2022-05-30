from http import HTTPStatus

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.permissions.permission_checks import is_permission_created, is_permission_updated
from base.api.users.permissions.permissions import get_permissions, get_permission, get_permissions_query, \
    create_permission, update_permission
from models.users.permission import get_default_permission, Permissions
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
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_PERMISSIONS.value)
@pytest.mark.parametrize('user_with_permissions_class', [Permissions.SCOPE], indirect=['user_with_permissions_class'])
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForPermissionsApi(BaseAPI):
    exclude = ['permissions', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    permission_id = cache_callable(get_default_permission)
    permission_payload = Permissions

    @allure.id("1818")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1272', name='[MailSender] 500 error when creating user')
    @allure.title('Check permissions for "Permissions" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_permissions, 'args': (), 'response': HTTPStatus.OK},
        {'method': get_permission, 'args': (permission_id,), 'response': HTTPStatus.OK},
        {'method': get_permissions_query, 'args': ('?skip=0&take=10&requireTotalCount=true',),
         'response': HTTPStatus.OK},
        {'method': create_permission, 'args': (permission_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': update_permission, 'args': (permission_id, permission_payload), 'response': HTTPStatus.ACCEPTED},
        {'method': is_permission_created, 'args': (permission_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_permission_updated, 'args': (permission_id,), 'response': HTTPStatus.NOT_FOUND},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_permissions_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
