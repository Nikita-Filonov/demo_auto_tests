import allure
import pytest
from alms_integration import create_activity

from base.api.base import BaseAPI
from base.api.users.activities.activities import get_activities, get_activity, update_activity, \
    get_activities_query
from models.users.activity import Activities, TextActivity
from parameters.api.users.activities import activity_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.activities import check_activity_response
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.activities
@allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1429', name='[Activity] Unable to set "content" to null')
@allure.epic('Core LMS')
@allure.feature('Activities')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestActivitiesApi(BaseAPI):
    activity = Activities.manager
    ACTIVITY_MODELS = [TextActivity(), Activities()]

    @allure.id("444")
    @allure.title('Get activities (API)')
    def test_get_activities(self):
        response = get_activities()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.activity.to_array_schema)

    @allure.id("479")
    @allure.title('Get activity (API)')
    @pytest.mark.parametrize('activity_function', ACTIVITY_MODELS, indirect=['activity_function'])
    def test_get_activity(self, activity_function):
        model, activity = activity_function

        response = get_activity(activity['id'])
        json_response = response.json()

        self.assert_attr(json_response['id'], activity['id'], Activities.activity_id.json)
        check_activity_response(response, activity, model)

    @allure.id("476")
    @allure.title('Create activity (API)')
    @pytest.mark.parametrize('activity', ACTIVITY_MODELS)
    def test_create_activity(self, activity):
        payload = activity.manager.to_json

        response = create_activity(payload)
        json_response = response.json()

        self.assert_attr(json_response['id'], payload['id'], activity.activity_id.json)
        check_activity_response(response, payload, activity)

    @allure.id("439")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1343', name='[Activity][API] Unable to update activity')
    @allure.title('Update activity (API)')
    @pytest.mark.parametrize('activity_function', ACTIVITY_MODELS, indirect=['activity_function'])
    def test_update_activity(self, activity_function):
        model, activity = activity_function

        payload = {
            **model.manager.to_json,
            Activities.tool_url.json: activity[Activities.tool_url.json],
            Activities.tool_resource_id.json: activity[Activities.tool_resource_id.json],
            Activities.lti_version.json: activity[Activities.lti_version.json],
        }

        response = update_activity(activity['id'], payload)
        json_response = response.json()

        self.assert_attr(json_response['id'], activity['id'], Activities.activity_id.json)
        check_activity_response(response, payload, model)

    @allure.id("1888")
    @pytest.mark.parametrize('query', to_sort_query(activity.to_json, exclude=activity.related_fields()))
    @allure.title('Query activities (API)')
    def test_query_activities(self, query):
        response = get_activities_query(query)
        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("901")
    @allure.title('Check authorization for activities endpoints (API)')
    @pytest.mark.parametrize('endpoint', activity_methods, ids=to_method_param)
    def test_check_authorization_for_activities_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
