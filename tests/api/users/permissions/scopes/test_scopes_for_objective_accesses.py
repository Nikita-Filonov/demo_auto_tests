from http import HTTPStatus

import allure
import pytest
from alms_integration import create_objective_access

from base.api.base import BaseAPI
from base.api.users.objectives.objective_accesses import get_objective_accesses, get_objective_access, \
    delete_objective_access
from base.api.users.objectives.objective_accesses_check import is_objective_access_created, is_objective_access_deleted
from models.users.objective_access import ObjectiveAccesses, get_default_objective_access
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
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_OBJECTIVE_ACCESSES.value)
@pytest.mark.parametrize(
    'user_with_permissions_class',
    [ObjectiveAccesses.SCOPE],
    indirect=['user_with_permissions_class']
)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForObjectiveAccessesApi(BaseAPI):
    exclude = ['objective_accesses', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    objective_access_id = cache_callable(get_default_objective_access)
    objective_access_payload = ObjectiveAccesses

    @allure.id("1827")
    @allure.title('Check permissions for "ObjectiveAccesses" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_objective_accesses, 'args': (), 'response': HTTPStatus.OK},
        {'method': get_objective_access, 'args': (objective_access_id,), 'response': HTTPStatus.OK},
        {'method': create_objective_access, 'args': (objective_access_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': delete_objective_access, 'args': (objective_access_id,), 'response': HTTPStatus.ACCEPTED},
        {'method': is_objective_access_created, 'args': (objective_access_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_objective_access_deleted, 'args': (objective_access_id,), 'response': HTTPStatus.NOT_FOUND},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_objective_accesses_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
