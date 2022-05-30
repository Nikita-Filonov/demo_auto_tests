from http import HTTPStatus

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.resource_libraries.resource_libraries import get_resource_library, get_resource_libraries, \
    create_resource_library, update_resource_library, delete_resource_library
from base.api.users.resource_libraries.resource_libraries_checks import is_resource_library_created, \
    is_resource_library_updated, is_resource_library_deleted
from models.users.resource_libraries import ResourceLibraries, get_default_resource_library, ResourceLibrariesLTI13
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
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_RESOURCE_LIBRARIES.value)
@pytest.mark.parametrize(
    'user_with_permissions_class',
    [[*ResourceLibraries.SCOPE]],
    indirect=['user_with_permissions_class']
)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForResourceLibrariesApi(BaseAPI):
    exclude = ['resource_libraries', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    resource_library_id = cache_callable(get_default_resource_library)
    resource_library_payload = ResourceLibrariesLTI13

    @allure.id("4428")
    @allure.title('Check permissions for "Resource libraries" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_resource_library, 'args': (resource_library_id,), 'response': HTTPStatus.OK},
        {'method': get_resource_libraries, 'args': (), 'response': HTTPStatus.OK},
        {'method': create_resource_library, 'args': (resource_library_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': update_resource_library, 'args': (resource_library_id, ResourceLibraries.manager.to_json),
         'response': HTTPStatus.ACCEPTED},
        {'method': delete_resource_library, 'args': (resource_library_id,), 'response': HTTPStatus.ACCEPTED},
        {'method': is_resource_library_created, 'args': (resource_library_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_resource_library_updated, 'args': (resource_library_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_resource_library_deleted, 'args': (resource_library_id,), 'response': HTTPStatus.NOT_FOUND},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_resource_library_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
