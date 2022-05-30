from http import HTTPStatus

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.objectives.objective_workflow_aggregates import get_objective_workflow_aggregates
from models.users.objective_workflow_aggregate import get_default_objective_workflow_aggregate, \
    ObjectiveWorkflowAggregates
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
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_OBJECTIVE_WORKFLOW_AGGREGATES.value)
@pytest.mark.parametrize(
    'user_with_permissions_class',
    [ObjectiveWorkflowAggregates.SCOPE],
    indirect=['user_with_permissions_class']
)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForObjectiveWorkflowAggregatesApi(BaseAPI):
    exclude = ['objective_workflow_aggregates', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    objective_workflow_aggregate_id = cache_callable(get_default_objective_workflow_aggregate)

    @allure.id("1830")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1272', name='[MailSender] 500 error when creating user')
    @allure.title('Check permissions for "ObjectiveWorkflowAggregates" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_objective_workflow_aggregates, 'args': (), 'response': HTTPStatus.OK},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_objective_workflow_aggregates_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
