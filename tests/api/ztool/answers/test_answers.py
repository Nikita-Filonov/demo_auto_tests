import allure
import pytest

from base.api.base import BaseAPI
from base.api.ztool.answers import create_answer, update_answer, delete_answer, get_answer
from models.ztool.answer import Answers
from settings import RERUNS, RERUNS_DELAY
from utils.api.ztool.permissions import permission_error


@allure.issue(
    url='https://youtrack.alemira.dev/issue/ALMS-1107',
    name='204 response code on GET to /api/v1/objectives/{id}/objective-workflow-aggregate'
)
@pytest.mark.api
@pytest.mark.answers
@allure.epic('Core LMS')
@allure.feature('Answers')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestAnswersApi(BaseAPI):
    answer = Answers.manager

    @allure.id("1915")
    @allure.title('Create answer (API)')
    def test_create_answer(self, learner, exercise):
        answer_payload = self.answer.to_json
        answer_payload['exerciseId'] = exercise['data']['id']
        answer_payload['workflowId'] = learner['workflow_id']
        response = create_answer(learner['request_id'], answer_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['exerciseId'], exercise['data']['id'], Answers.exercise_id.json)
        self.assert_attr(json_response['workflowId'], learner['workflow_id'], Answers.workflow_id.json)
        self.assert_attr(json_response['text'], answer_payload['text'], Answers.text.json)
        self.validate_json(json_response, self.answer.to_schema)

    @allure.id("1913")
    @allure.title('Update answer (API)')
    def test_update_answer(self, answer):
        answer_payload = self.answer.to_json
        response = update_answer(answer['request_id'], answer['data']['id'], answer_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], answer['data']['id'], Answers.answer_id.json)
        self.assert_attr(json_response['text'], answer_payload['text'], Answers.text.json)
        self.assert_attr(json_response['exerciseId'], answer['data']['exerciseId'], Answers.exercise_id.json)
        self.assert_attr(json_response['workflowId'], answer['data']['workflowId'], Answers.workflow_id.json)
        self.validate_json(json_response, self.answer.to_schema)

    @allure.id("1916")
    @allure.title('Delete answer (API)')
    def test_delete_answer(self, answer):
        response = delete_answer(answer['request_id'], answer['data']['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.FORBIDDEN)
        self.assert_json(json_response, permission_error('Delete'))

    @allure.id("1912")
    @allure.title('Get answer (API)')
    def test_get_answer(self, answer):
        response = get_answer(answer['request_id'], answer['data']['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], answer['data']['id'], Answers.answer_id.json)
        self.assert_attr(json_response['text'], answer['data']['text'], Answers.text.json)
        self.assert_attr(json_response['exerciseId'], answer['exercise_id'], Answers.exercise_id.json)
        self.assert_attr(json_response['workflowId'], answer['workflow_id'], Answers.workflow_id.json)
        self.validate_json(json_response, self.answer.to_schema)
