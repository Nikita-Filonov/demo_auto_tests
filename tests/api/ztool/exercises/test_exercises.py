from http import HTTPStatus

import allure
import pytest

from base.api.base import BaseAPI
from base.api.ztool.exercises import create_exercise, update_exercise, delete_exercise, get_exercise
from models.users.role import SupportedRoles
from models.ztool.exercise import Exercises
from settings import RERUNS, RERUNS_DELAY
from utils.api.ztool.permissions import permission_error


@allure.issue(
    url='https://youtrack.alemira.dev/issue/ALMS-1107',
    name='204 response code on GET to /api/v1/objectives/{id}/objective-workflow-aggregate'
)
@pytest.mark.api
@pytest.mark.exercises
@allure.epic('Core LMS')
@allure.feature('Exercises')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestExercisesApi(BaseAPI):
    exercise = Exercises.manager

    ROLES_CAN_CHANGE_EXERCISE = [SupportedRoles.AUTHOR]
    ROLES_CAN_NOT_CHANGE_EXERCISE = [SupportedRoles.LEARNER, SupportedRoles.INSTRUCTOR]

    @allure.id("1930")
    @allure.title('Create exercise (API)')
    def test_create_exercise(self, author: dict):
        exercise_payload = self.exercise.to_json
        exercise_payload['elementId'] = author['element_id']
        response = create_exercise(author['request_id'], exercise_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, HTTPStatus.OK)
        self.assert_attr(json_response['id'], exercise_payload['id'], Exercises.exercise_id.json)
        self.assert_attr(json_response['elementId'], author['element_id'], Exercises.exercise_id.json)
        self.assert_attr(json_response['maxScore'], exercise_payload['maxScore'], Exercises.max_score.json)
        self.assert_attr(json_response['slug'], exercise_payload['slug'], Exercises.slug.json)
        self.assert_attr(json_response['text'], exercise_payload['text'], Exercises.text.json)
        self.assert_attr(json_response['group'], exercise_payload['group'], Exercises.group.json)
        self.assert_attr(json_response['order'], exercise_payload['order'], Exercises.order.json)
        self.assert_attr(json_response['correctAnswer'], exercise_payload['correctAnswer'],
                         Exercises.correct_answer.json)
        self.assert_attr(json_response['tutorGuideline'], exercise_payload['tutorGuideline'],
                         Exercises.tutor_guideline.json)
        self.validate_json(json_response, self.exercise.to_schema)

    @allure.id("1936")
    @allure.title('Create exercise negative (API)')
    @pytest.mark.parametrize('launch', ROLES_CAN_CHANGE_EXERCISE, indirect=['launch'])
    def test_create_exercise_negative(self, launch: dict):
        response = create_exercise(launch['request_id'], {})
        error_message = response.json()['common'][0]
        expected_message = "Element with Id '00000000-0000-0000-0000-000000000000' " \
                           "does not exist or your permissions are not enough to access it"

        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)
        self.assert_attr(error_message['message'], expected_message, 'Error message')

    @allure.id("1932")
    @allure.title('Create exercise without permissions (API)')
    @pytest.mark.parametrize('launch', ROLES_CAN_NOT_CHANGE_EXERCISE, indirect=['launch'])
    def test_create_exercise_without_permissions(self, launch: dict):
        exercise_payload = self.exercise.to_json
        exercise_payload['elementId'] = launch['element_id']
        response = create_exercise(launch['request_id'], exercise_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.FORBIDDEN)
        self.assert_json(json_response, permission_error('Create'))

    @allure.id("1931")
    @allure.title('Update exercise without permissions (API)')
    @pytest.mark.parametrize('launch', ROLES_CAN_NOT_CHANGE_EXERCISE, indirect=['launch'])
    def test_update_exercise_without_permissions(self, exercise, launch: dict):
        request_id = launch['request_id']
        exercise_id = exercise['data']['id']
        exercise_payload = self.exercise.to_json
        response = update_exercise(request_id, exercise_id, exercise_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.FORBIDDEN)
        self.assert_json(json_response, permission_error('Update'))

    @allure.id("1935")
    @allure.title('Delete exercise without permissions (API)')
    @pytest.mark.parametrize('launch', ROLES_CAN_NOT_CHANGE_EXERCISE, indirect=['launch'])
    def test_delete_exercise_without_permissions(self, exercise, launch: dict):
        request_id = launch['request_id']
        exercise_id = exercise['data']['id']

        response = delete_exercise(request_id, exercise_id)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.FORBIDDEN)
        self.assert_json(json_response, permission_error('Delete'))

    @allure.id("1929")
    @allure.title('Update exercise (API)')
    def test_update_exercise(self, exercise):
        request_id = exercise['request_id']
        exercise_id = exercise['data']['id']
        exercise_payload = self.exercise.to_json
        response = update_exercise(request_id, exercise_id, exercise_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], exercise_id, Exercises.exercise_id.json)
        self.assert_attr(json_response['elementId'], exercise['element_id'], Exercises.exercise_id.json)
        self.assert_attr(json_response['maxScore'], exercise_payload['maxScore'], Exercises.max_score.json)
        self.assert_attr(json_response['slug'], exercise_payload['slug'], Exercises.slug.json)
        self.assert_attr(json_response['text'], exercise_payload['text'], Exercises.text.json)
        self.assert_attr(json_response['group'], exercise_payload['group'], Exercises.group.json)
        self.assert_attr(json_response['order'], exercise_payload['order'], Exercises.order.json)
        self.assert_attr(json_response['correctAnswer'], exercise_payload['correctAnswer'],
                         Exercises.correct_answer.json)
        self.assert_attr(json_response['tutorGuideline'], exercise_payload['tutorGuideline'],
                         Exercises.tutor_guideline.json)
        self.validate_json(json_response, self.exercise.to_schema)

    @allure.id("1928")
    @allure.title('Delete exercise (API)')
    def test_delete_exercise(self, exercise):
        request_id = exercise['request_id']
        exercise_id = exercise['data']['id']

        response = delete_exercise(request_id, exercise_id)
        is_exercise_exists = self.exercise.is_exists(exercise_id=exercise_id)

        self.assert_response_status(response.status_code, self.http.OK)
        assert not is_exercise_exists

    @allure.id("1927")
    @allure.title('Get exercise (API)')
    def test_get_exercise(self, exercise):
        request_id = exercise['request_id']
        exercise_payload = exercise['data']

        response = get_exercise(request_id, exercise_payload['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_json(exercise_payload, json_response)
        self.validate_json(json_response, self.exercise.to_schema)
