from http import HTTPStatus

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.groups.group_checks import is_group_created, is_group_deleted, is_group_updated
from base.api.users.groups.groups import get_group, get_groups, update_group, delete_group, create_group
from models.users.group import Groups, get_default_group
from models.users.role import Roles
from models.utils.users.roles import filter_scopes
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
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_GROUPS.value)
@pytest.mark.parametrize(
    'user_with_permissions_class',
    [[*Groups.SCOPE, *filter_scopes(Roles.SCOPE, None, 'Create')]],
    indirect=['user_with_permissions_class']
)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForGroupsApi(BaseAPI):
    exclude = ['groups', 'roles.is_role_created', 'roles.create_role', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    group_id = cache_callable(get_default_group)
    group_payload = Groups

    @allure.id("1816")
    @allure.title('Check permissions for "Groups" model (API)')
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-600',
        name='Nothing returned in validationDictionary for api/v1/groups'
    )
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-992',
        name='Command to create group not finished successfully'
    )
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1275',
        name='User with permissions for "Groups" has access to "GroupUsers"'
    )
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1276',
        name='User with permissions for "Groups" has access to "UserRoles"'
    )
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1277',
        name='User with permissions for "Groups" has access to "Users"'
    )
    @pytest.mark.parametrize('endpoint', [
        {'method': get_group, 'args': (group_id,), 'response': HTTPStatus.OK},
        {'method': get_groups, 'args': (), 'response': HTTPStatus.OK},
        {'method': create_group, 'args': (group_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': update_group, 'args': (group_id, group_payload), 'response': HTTPStatus.ACCEPTED},
        {'method': delete_group, 'args': (group_id,), 'response': HTTPStatus.ACCEPTED},
        {'method': is_group_created, 'args': (group_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_group_updated, 'args': (group_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_group_deleted, 'args': (group_id,), 'response': HTTPStatus.NOT_FOUND},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_groups_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
