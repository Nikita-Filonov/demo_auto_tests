from http import HTTPStatus

import allure
import pytest
from alms_integration import start_objective_workflow, get_objective_workflows

from base.api.base import BaseAPI
from base.api.users.objectives.objective_workflows import get_objective_workflow, get_started_objective_workflow, \
    get_started_objective_workflows, submit_objective_workflow, get_submitted_objective_workflow, \
    get_submitted_objective_workflows
from models.users.objective_workflow import get_default_objective_workflow, ObjectiveWorkflows
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
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_OBJECTIVE_WORKFLOWS.value)
@pytest.mark.parametrize(
    'user_with_permissions_class',
    [ObjectiveWorkflows.SCOPE],
    indirect=['user_with_permissions_class']
)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForObjectiveWorkflowsApi(BaseAPI):
    exclude = ['objective_workflows', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    objective_workflow_id = cache_callable(get_default_objective_workflow)

    @allure.id("1824")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1272', name='[MailSender] 500 error when creating user')
    @allure.title('Check permissions for "ObjectiveWorkflows" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_objective_workflows, 'args': (), 'response': HTTPStatus.OK},
        {'method': get_objective_workflow, 'args': (objective_workflow_id,), 'response': HTTPStatus.OK},
        {'method': start_objective_workflow, 'args': ({},), 'response': HTTPStatus.ACCEPTED},
        {'method': get_started_objective_workflow, 'args': (objective_workflow_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': get_started_objective_workflows, 'args': (), 'response': HTTPStatus.OK},
        {'method': submit_objective_workflow, 'args': ({},), 'response': HTTPStatus.NOT_FOUND},
        {'method': get_submitted_objective_workflow, 'args': (objective_workflow_id,),
         'response': HTTPStatus.NOT_FOUND},
        {'method': get_submitted_objective_workflows, 'args': (), 'response': HTTPStatus.OK},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_objective_workflows_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
