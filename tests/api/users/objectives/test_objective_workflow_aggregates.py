import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.objectives.objective_workflow_aggregates import get_objective_workflow_aggregates_query
from models.users.objective_workflow_aggregate import ObjectiveWorkflowAggregates
from parameters.api.users.objective_workflow_aggregates import objective_workflow_aggregate_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.objective_workflow_aggregates
@allure.epic('Core LMS')
@allure.feature('Objectives objective workflow aggregates')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestObjectivesWorkflowAggregatesApi(BaseAPI):
    objective_workflow_aggregate = ObjectiveWorkflowAggregates.manager

    @allure.id("1890")
    @allure.title('Get objective workflow aggregates query')
    @pytest.mark.parametrize('query', to_sort_query(objective_workflow_aggregate.to_json,
                                                    exclude=objective_workflow_aggregate.related_fields()))
    def test_get_objective_workflow_aggregates_query(self, query):
        response = get_objective_workflow_aggregates_query(query)
        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("4081")
    @allure.title('Check authorization for objective workflow aggregates endpoints (API)')
    @pytest.mark.parametrize('endpoint', objective_workflow_aggregate_methods, ids=to_method_param)
    def test_check_authorization_for_objective_workflow_aggregates(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
