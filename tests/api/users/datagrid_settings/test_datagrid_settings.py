import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.datagrid_settings.datagrid_settings import get_data_grid_settings, create_data_grid_setting, \
    delete_data_grid_setting, get_data_grid_setting
from models.users.data_grid_settings import DataGridSettings
from parameters.api.users.data_grid_settings import data_grid_settings_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.formatters.parametrization import to_method_param
from utils.utils import random_string


@allure.issue(
    url='https://youtrack.alemira.dev/issue/ALMS-594',
    name='GET on /api/v1/datagrid-settings returns 500 status code'
)
@pytest.mark.api
@pytest.mark.datagrid_settings
@allure.epic('Core LMS')
@allure.feature('Datagrid settings')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestDataGridSettingsApi(BaseAPI):
    data_grid_settings = DataGridSettings.manager

    @allure.id("523")
    @allure.title('Get datagrid settings (API)')
    def test_get_datagrid_settings(self):
        response = get_data_grid_settings()
        self.assert_response_status(response.status_code, self.http.OK)

    @allure.id("522")
    @allure.title('Create datagrid setting (API)')
    def test_create_datagrid_setting(self):
        payload = self.data_grid_settings.to_json
        response = create_data_grid_setting(payload)
        json_response = response.json()

        self.assert_attr(json_response['key'], payload['key'], 'key')
        self.assert_attr(json_response['settings'], payload['settings'], 'settings')
        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.data_grid_settings.to_schema)

    @allure.id("526")
    @allure.title('Create datagrid setting negative (API)')
    def test_create_datagrid_setting_negative(self):
        payload = self.data_grid_settings.to_negative_json()

        response = create_data_grid_setting(payload)
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)

    @allure.id("525")
    @allure.title('Delete datagrid setting (API)')
    def test_delete_datagrid_setting(self, data_grid_settings):
        response = delete_data_grid_setting(data_grid_settings['key'])
        self.assert_response_status(response.status_code, self.http.OK)

    @allure.id("525")
    @allure.title('Get datagrid setting (API)')
    def test_get_datagrid_setting(self, data_grid_settings):
        response = get_data_grid_setting(data_grid_settings['key'])
        json_response = response.json()

        self.assert_attr(json_response['key'], data_grid_settings['key'], 'key')
        self.assert_attr(json_response['settings'], data_grid_settings['settings'], 'settings')
        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.data_grid_settings.to_schema)

    @allure.id("520")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-255',
        name='GET /datagrid-settings/{key} returns 204 instead of 404'
    )
    @allure.title('Get datagrid setting negative (API)')
    def test_get_datagrid_setting_negative(self):
        response = get_data_grid_setting(random_string())
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("524")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-254',
        name='DELETE /datagrid-settings/{key} returns 200 instead of 404'
    )
    @allure.title('Delete datagrid setting negative (API)')
    def test_delete_datagrid_setting_negative(self):
        response = delete_data_grid_setting(random_string())
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("907")
    @allure.title('Check authorization for datagrid settings endpoints (API)')
    @pytest.mark.parametrize('endpoint', data_grid_settings_methods, ids=to_method_param)
    def test_check_authorization_for_datagrid_settings_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
