import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.reports.reports import get_for_grading_reports, get_payroll_reports, get_user_reports, \
    get_not_started_reports, get_objective_reports
from models.utils.users.query import SortModel
from settings import RERUNS, RERUNS_DELAY
from utils.api.utils import to_pagination_query


@pytest.mark.api
@pytest.mark.reports
@allure.epic('Core LMS')
@allure.feature('Reports')
@pytest.mark.parametrize('query', to_pagination_query())
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestReportsApi(BaseAPI):

    @allure.id("4423")
    @allure.title('Get for grading reports (API)')
    def test_get_for_grading_reports(self, query):
        response = get_for_grading_reports(query)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_lte(len(json_response[SortModel.data.json]), query['take'], 'Reports count')
        self.validate_json(json_response, self.sort_model_users.to_schema)

    @allure.id("4426")
    @allure.title('Get payroll reports (API)')
    def test_get_payroll_reports(self, query):
        response = get_payroll_reports(query)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_lte(len(json_response[SortModel.data.json]), query['take'], 'Reports count')
        self.validate_json(json_response, self.sort_model_users.to_schema)

    @allure.id("4424")
    @allure.title('Get user reports (API)')
    def test_get_user_reports(self, query):
        response = get_user_reports(query)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_lte(len(json_response[SortModel.data.json]), query['take'], 'Reports count')
        self.validate_json(json_response, self.sort_model_users.to_schema)

    @allure.id("4425")
    @allure.title('Get not started reports (API)')
    def test_get_not_started_reports(self, query):
        response = get_not_started_reports(query)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_lte(len(json_response[SortModel.data.json]), query['take'], 'Reports count')
        self.validate_json(json_response, self.sort_model_users.to_schema)

    @allure.title('Get objective reports (API)')
    def test_get_objective_reports(self, query):
        response = get_objective_reports(query)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_lte(len(json_response[SortModel.data.json]), query['take'], 'Reports count')
        self.validate_json(json_response, self.sort_model_users.to_schema)
