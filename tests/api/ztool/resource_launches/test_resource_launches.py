import allure
import pytest

from base.api.base import BaseAPI
from base.api.ztool.launch import get_launch_request
from models.users.role import SupportedRoles
from models.ztool.resource_launch import ResourceLaunches
from settings import RERUNS, RERUNS_DELAY, LEARNER_URL, ADMIN_URL
from tests.api.ztool.conftest import ROLES


@pytest.mark.api
@pytest.mark.resource_launches
@allure.epic('Core LMS')
@allure.feature('Launch')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestResourceLaunchesApi(BaseAPI):
    RETURN_URLS = {
        SupportedRoles.AUTHOR.value: ADMIN_URL + '/lti-tool-callback.html',
        SupportedRoles.INSTRUCTOR.value: ADMIN_URL + '/lti-tool-callback.html',
        SupportedRoles.LEARNER.value: LEARNER_URL + '/lti-tool-callback.html'
    }
    resource_launch = ResourceLaunches.manager

    @allure.id("1954")
    @allure.title('Generate request id')
    @pytest.mark.parametrize('launch', ROLES, indirect=['launch'])
    def test_generate_request_id(self, launch: dict):
        database_launch = self.resource_launch.get(resource_launch_id=launch['request_id'])

        self.assert_attr(launch['element_id'], database_launch['element_id'], ResourceLaunches.element_id.json)
        self.assert_attr(launch['objective_id'], database_launch['context_id'], ResourceLaunches.context_id.json)
        self.assert_attr(launch['workflow_id'], database_launch['workflow_id'], ResourceLaunches.workflow_id.json)
        self.assert_attr(launch['role'], database_launch['roles'], ResourceLaunches.roles.json)
        self.assert_attr(launch['workflow_id'], database_launch['resource_id'], ResourceLaunches.roles.json)
        self.assert_attr(launch['request_id'], database_launch['resource_launch_id'],
                         ResourceLaunches.resource_launch_id.json)

    @allure.id("1955")
    @allure.title('Get launch request')
    @pytest.mark.parametrize('launch', ROLES, indirect=['launch'])
    def test_get_launch_request(self, launch: dict):
        response = get_launch_request(launch['request_id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['elementId'], launch['element_id'], ResourceLaunches.element_id.json)
        self.assert_attr(json_response['workflowId'], launch['workflow_id'], ResourceLaunches.workflow_id.json)
        self.assert_attr(json_response['id'], launch['request_id'], ResourceLaunches.resource_launch_id.json)
        self.assert_attr(json_response['returnUrl'], self.RETURN_URLS[launch['role']], 'returnUrl')
