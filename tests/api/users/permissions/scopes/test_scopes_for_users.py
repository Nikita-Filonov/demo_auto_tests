from http import HTTPStatus

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.users.user_checks import is_user_created, is_user_updated
from base.api.users.users.users import get_users, get_user, create_user, update_user
from models.users.user import Users, get_default_user
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
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_USERS.value)
@pytest.mark.parametrize('user_with_permissions_class', [Users.SCOPE], indirect=['user_with_permissions_class'])
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForUsersApi(BaseAPI):
    exclude = ['users', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    user_id = cache_callable(get_default_user)
    user_payload = Users

    @allure.id("1820")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-610',
        name='User with permissions for "Users" has access to "UserRoles"'
    )
    @allure.title('Check permissions for "Users" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_users, 'args': (), 'response': HTTPStatus.OK},
        {'method': get_user, 'args': (user_id,), 'response': HTTPStatus.OK},
        {'method': create_user, 'args': (user_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': update_user, 'args': (user_id, user_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': is_user_created, 'args': (user_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_user_updated, 'args': (user_id,), 'response': HTTPStatus.NOT_FOUND},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_users_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
