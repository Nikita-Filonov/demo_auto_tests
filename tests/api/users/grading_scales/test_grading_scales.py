import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.grading_scales.grading_scales import get_grading_scales, create_grading_scale, update_grading_scale, \
    get_grading_scale, delete_grading_scale
from models.users.grades import Grades, MIN_NUMBER_OF_GRADES
from models.users.grading_scale import GradingScales
from parameters.api.users.grading_scales import grading_scales_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.grading_scales import normalized_grading_scales_grades, \
    check_grading_scales_response, denormalized_grading_scales_grades
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.formatters.parametrization import to_method_param
from utils.utils import random_number


@pytest.mark.api
@pytest.mark.grading_scales
@allure.epic('Core LMS')
@allure.feature('Grading scales')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestGradingScalesApi(BaseAPI):
    grade = Grades.manager
    grading_scale = GradingScales.manager
    NEGATIVE_GRADES = [
        [],
        normalized_grading_scales_grades(MIN_NUMBER_OF_GRADES - 1),
        denormalized_grading_scales_grades(4),
        denormalized_grading_scales_grades(4, max_score=-random_number())
    ]
    NEGATIVE_GRADES_IDS = [
        'Empty grades',
        'Grades less than max',
        'Grades with repeated "name", "maxScore"',
        'Grades with repeated "name", "maxScore" and negative "maxScore"'
    ]

    @allure.id("4662")
    @allure.title('Get grading scales (API)')
    def test_get_grading_scales(self):
        response = get_grading_scales()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.grading_scale.to_array_schema)

    @allure.id("4656")
    @allure.title('Create grading scale (API)')
    def test_create_grading_scale(self):
        grading_scale_payload = self.grading_scale.to_json
        response = create_grading_scale(grading_scale_payload)

        check_grading_scales_response(response, grading_scale_payload)

    @allure.id("4659")
    @allure.title('Update grading scale (API)')
    @pytest.mark.parametrize('grades', [normalized_grading_scales_grades(4)])
    def test_update_grading_scale(self, grading_scale, grades):
        grading_scale_payload = {**self.grading_scale.to_json, GradingScales.grades.json: grades}
        response = update_grading_scale(grading_scale['id'], grading_scale_payload)

        check_grading_scales_response(response, grading_scale_payload)

    @allure.id("4661")
    @allure.title('Get grading scale (API)')
    def test_get_grading_scale(self, grading_scale):
        response = get_grading_scale(grading_scale['id'])

        check_grading_scales_response(response, grading_scale)

    @allure.id("4654")
    @allure.title('Delete grading scale (API)')
    def test_delete_grading_scale(self, grading_scale):
        response = delete_grading_scale(grading_scale['id'])
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("4660")
    @allure.title('Create grading scale negative (API)')
    def test_create_grading_scale_negative(self):
        grading_scale_payload = self.grading_scale.to_negative_json()
        response = create_grading_scale(grading_scale_payload)
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)

    @allure.id("4657")
    @allure.title('Create grading scale with negative grades (API)')
    @pytest.mark.parametrize('grades', NEGATIVE_GRADES, ids=NEGATIVE_GRADES_IDS)
    def test_create_grading_scale_with_negative_grades(self, request, grades):
        allure.dynamic.description(request.node.callspec.id)
        grading_scale_payload = {**self.grading_scale.to_json, GradingScales.grades.json: grades}
        response = create_grading_scale(grading_scale_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['completed']['state'], self.state.FAILED.value, 'Response state')

    @allure.id("4655")
    @allure.title('Update grading scale with negative grades (API)')
    @pytest.mark.parametrize('grades', NEGATIVE_GRADES, ids=NEGATIVE_GRADES_IDS)
    def test_update_grading_scale_with_negative_grades(self, request, grades, grading_scale):
        allure.dynamic.description(request.node.callspec.id)
        grading_scale_payload = {**self.grading_scale.to_json, GradingScales.grades.json: grades}
        response = update_grading_scale(grading_scale['id'], grading_scale_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['completed']['state'], self.state.FAILED.value, 'Response state')

    @allure.id("4658")
    @allure.title('Check authorization for grading scales endpoints (API)')
    @pytest.mark.parametrize('endpoint', grading_scales_methods, ids=to_method_param)
    def test_check_authorization_for_grading_scales_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
