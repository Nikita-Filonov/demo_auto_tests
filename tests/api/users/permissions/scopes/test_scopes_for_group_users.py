from http import HTTPStatus

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.group_users.group_user_checks import is_group_user_created, is_group_user_deleted
from base.api.users.group_users.group_users import get_group_users, get_group_user, create_group_user, \
    delete_group_user, get_group_users_query
from models.users.group_user import get_default_group_user, GroupUsers
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
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_GROUP_USERS.value)
@pytest.mark.parametrize('user_with_permissions_class', [GroupUsers.SCOPE], indirect=['user_with_permissions_class'])
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForGroupUsersApi(BaseAPI):
    exclude = ['group_users', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    group_user_id = cache_callable(get_default_group_user)
    group_user_payload = GroupUsers

    @allure.id("1823")
    @allure.title('Check permissions for "GroupUsers" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_group_users, 'args': (), 'response': HTTPStatus.OK},
        {'method': get_group_user, 'args': (group_user_id,), 'response': HTTPStatus.OK},
        {'method': create_group_user, 'args': (group_user_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': delete_group_user, 'args': (group_user_id,), 'response': HTTPStatus.ACCEPTED},
        {'method': is_group_user_created, 'args': (group_user_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_group_user_deleted, 'args': (group_user_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': get_group_users_query, 'args': ('?skip=0&take=10&requireTotalCount=true',),
         'response': HTTPStatus.OK},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_group_users_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
