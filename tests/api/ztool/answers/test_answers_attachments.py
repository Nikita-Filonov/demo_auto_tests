import os

import allure
import pytest

from base.api.base import BaseAPI
from base.api.ztool.answers import attach_file_to_answer, get_answer, get_attachment_link_from_answer, \
    update_attachment_in_answer, delete_attachment_from_answer, upload_feedback_attachment_to_answer, \
    delete_feedback_attachment_from_answer, update_feedback_attachment_in_answer, \
    get_feedback_attachment_link_from_answer
from models.ztool.answer import Answers
from models.ztool.attachment import AnswerAttachments
from parameters.courses.ui.ztool.answers import answers_properties
from parameters.courses.ui.ztool.attachments import feedback_attachments_properties, answer_attachments_properties
from parameters.courses.ui.ztool.exercises import exercises_properties
from settings import RERUNS, RERUNS_DELAY
from tests.api.ztool.conftest import EXCLUDE_FILES
from utils.allure.stories.api.ztool.answers import AnswersStory
from utils.api.utils import get_default_files, download_file


@allure.issue(
    url='https://youtrack.alemira.dev/issue/ALMS-1107',
    name='204 response code on GET to /api/v1/objectives/{id}/objective-workflow-aggregate'
)
@pytest.mark.api
@pytest.mark.answers_attachments
@allure.epic('Core LMS')
@allure.feature('Answers')
@allure.story(AnswersStory.ANSWERS_ATTACHMENTS.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestAnswersAttachmentsApi(BaseAPI):
    answer = Answers.manager
    attachment = AnswerAttachments.manager
    files = get_default_files(EXCLUDE_FILES)
    WORKFLOW_WITH_ANSWER = [{'answers': [answers_properties[0]], 'exercises': [exercises_properties[0]]}]
    FEEDBACK_ATTACHMENT = [{'feedback_attachments': [feedback_attachments_properties[0]]}]
    WORKFLOW_WITH_ANSWER_AND_ATTACHMENT = [{
        'answers': [answers_properties[0]],
        'exercises': [exercises_properties[0]],
        'attachments': [answer_attachments_properties[0]]
    }]

    @allure.id("1914")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1672',
        name='[Attachments] 500 error when attaching file to the answer'
    )
    @allure.title('Upload attachment to answer (API)')
    @pytest.mark.parametrize('file_path', files)
    def test_upload_attachment_to_answer(self, answer, file_path):
        files = {'formFile': open(file_path, 'rb')}
        filename = os.path.basename(file_path)
        file_response = attach_file_to_answer(answer['request_id'], answer['data']['id'], files=files)

        answer_response = get_answer(answer['request_id'], answer['data']['id'])
        answer_json_response = answer_response.json()

        self.assert_response_status(file_response.status_code, self.http.OK)
        self.assert_response_status(answer_response.status_code, self.http.OK)
        self.assert_attr(len(answer_json_response['attachments']), 1, 'Number of attachments')
        self.assert_attr(answer_json_response['attachments'][0]['name'], filename, 'Attachment name')
        self.validate_json(answer_json_response, self.answer.to_schema)

    @allure.id("1920")
    @allure.title('Delete attachment from answer (API)')
    @pytest.mark.parametrize('started_workflow', WORKFLOW_WITH_ANSWER_AND_ATTACHMENT, indirect=['started_workflow'])
    def test_delete_attachment_from_answer(self, started_workflow, learner):
        request_id = learner['request_id']
        answer_id = started_workflow['answers'][0]['answer_id']
        attachment_id = started_workflow['attachments'][0]['answer_attachment_id']

        file_response = delete_attachment_from_answer(request_id, answer_id, attachment_id)

        answer_response = get_answer(request_id, answer_id)
        answer_json_response = answer_response.json()

        self.assert_response_status(file_response.status_code, self.http.OK)
        self.assert_response_status(answer_response.status_code, self.http.OK)
        self.assert_attr(len(answer_json_response[Answers.attachments.json]), 0, 'Number of attachments')
        self.validate_json(answer_json_response, self.answer.to_schema)

    @allure.id("1919")
    @allure.title('Update attachment in answer (API)')
    @pytest.mark.parametrize('order', [5])
    @pytest.mark.parametrize('started_workflow', WORKFLOW_WITH_ANSWER_AND_ATTACHMENT, indirect=['started_workflow'])
    def test_update_attachment_in_answer(self, started_workflow, order, learner):
        request_id = learner['request_id']
        answer_id = started_workflow['answers'][0]['answer_id']
        attachment_id = started_workflow['attachments'][0]['answer_attachment_id']
        payload = {**self.attachment.to_json, 'order': order}

        attachment_response = update_attachment_in_answer(request_id, answer_id, attachment_id, payload)
        answer_response = get_answer(request_id, answer_id)
        answer_json_response = answer_response.json()
        attachment = answer_json_response['attachments'][0]

        self.assert_response_status(answer_response.status_code, self.http.OK)
        self.assert_response_status(attachment_response.status_code, self.http.OK)
        self.assert_attr(answer_json_response['id'], answer_id, Answers.answer_id.json)
        self.assert_attr(attachment['id'], attachment_id, AnswerAttachments.answer_attachment_id.json)
        self.assert_attr(attachment['name'], payload['name'], AnswerAttachments.name.json)
        self.assert_attr(attachment['order'], order, AnswerAttachments.order.json)
        self.validate_json(answer_json_response, self.answer.to_schema)

    @allure.id("1922")
    @allure.title('Download attachment from answer (API)')
    @pytest.mark.parametrize('started_workflow', WORKFLOW_WITH_ANSWER_AND_ATTACHMENT, indirect=['started_workflow'])
    def test_download_attachment_from_answer(self, started_workflow, learner):
        original_file_name = started_workflow['attachments'][0]['name']
        request_id = learner['request_id']
        answer_id = started_workflow['answers'][0]['answer_id']
        attachment_id = started_workflow['attachments'][0]['answer_attachment_id']

        response = get_attachment_link_from_answer(request_id, answer_id, attachment_id)
        download_link = response.json()['url']
        file_path, downloaded_file_name = download_file(download_link)

        self.assert_attr(original_file_name, downloaded_file_name, 'File name')
        self.assert_downloaded_file(downloaded_file_name)

    @allure.id("4221")
    @allure.title('Upload feedback attachment to answer (API)')
    @pytest.mark.parametrize('file_path', files)
    @pytest.mark.parametrize('started_workflow', WORKFLOW_WITH_ANSWER, indirect=['started_workflow'])
    def test_upload_feedback_attachment_to_answer(self, file_path, started_workflow, in_grade_workflow, instructor):
        filename = os.path.basename(file_path)
        answer_id = started_workflow['answers'][0]['answer_id']
        file_response = upload_feedback_attachment_to_answer(instructor['request_id'], answer_id, file_path)

        answer_response = get_answer(instructor['request_id'], answer_id)
        answer_json_response = answer_response.json()

        self.assert_response_status(file_response.status_code, self.http.OK)
        self.assert_response_status(answer_response.status_code, self.http.OK)
        self.assert_attr(len(answer_json_response['feedbackAttachments']), 1, 'Number of feedback attachments')
        self.assert_attr(answer_json_response['feedbackAttachments'][0]['name'], filename, 'Feedback attachment name')
        self.validate_json(answer_json_response, self.answer.to_schema)

    @allure.id("4223")
    @allure.title('Delete feedback attachment from the answer (API)')
    @pytest.mark.parametrize('started_workflow', WORKFLOW_WITH_ANSWER, indirect=['started_workflow'])
    @pytest.mark.parametrize('submitted_workflow', FEEDBACK_ATTACHMENT, indirect=['submitted_workflow'])
    def test_delete_feedback_attachment_from_the_answer(self, submitted_workflow, in_grade_workflow, instructor,
                                                        started_workflow):
        answer_id = submitted_workflow['answers'][0]['answer_id']
        feedback_attachment_id = in_grade_workflow['feedback_attachments'][0]['answer_feedback_attachment_id']
        file_response = delete_feedback_attachment_from_answer(instructor['request_id'], answer_id,
                                                               feedback_attachment_id)

        answer_response = get_answer(instructor['request_id'], answer_id)
        answer_json_response = answer_response.json()

        self.assert_response_status(file_response.status_code, self.http.OK)
        self.assert_response_status(answer_response.status_code, self.http.OK)
        self.assert_attr(len(answer_json_response[Answers.feedback_attachments.json]), 0,
                         'Number of feedback attachments')
        self.validate_json(answer_json_response, self.answer.to_schema)

    @allure.id("4222")
    @allure.title('Update feedback attachment in the answer (API)')
    @pytest.mark.parametrize('order', [5])
    @pytest.mark.parametrize('started_workflow', WORKFLOW_WITH_ANSWER, indirect=['started_workflow'])
    @pytest.mark.parametrize('submitted_workflow', FEEDBACK_ATTACHMENT, indirect=['submitted_workflow'])
    def test_update_feedback_attachment_in_the_answer(self, submitted_workflow, in_grade_workflow, instructor, order,
                                                      started_workflow):
        request_id = instructor['request_id']
        answer_id = submitted_workflow['answers'][0]['answer_id']
        feedback_attachment_id = in_grade_workflow['feedback_attachments'][0]['answer_feedback_attachment_id']
        payload = {**self.attachment.to_json, 'order': order}
        file_response = update_feedback_attachment_in_answer(request_id, answer_id, feedback_attachment_id, payload)

        answer_response = get_answer(request_id, answer_id)
        answer_json_response = answer_response.json()
        feedback_attachment = answer_json_response[Answers.feedback_attachments.json][0]

        self.assert_response_status(file_response.status_code, self.http.OK)
        self.assert_response_status(answer_response.status_code, self.http.OK)
        self.assert_attr(answer_json_response['id'], answer_id, Answers.answer_id.json)
        self.assert_attr(feedback_attachment['id'], feedback_attachment_id, AnswerAttachments.answer_attachment_id.json)
        self.assert_attr(feedback_attachment['name'], payload['name'], AnswerAttachments.name.json)
        self.assert_attr(feedback_attachment['order'], order, AnswerAttachments.order.json)
        self.validate_json(answer_json_response, self.answer.to_schema)

    @allure.id("4224")
    @allure.title('Download feedback attachment from answer (API)')
    @pytest.mark.parametrize('started_workflow', WORKFLOW_WITH_ANSWER, indirect=['started_workflow'])
    @pytest.mark.parametrize('submitted_workflow', FEEDBACK_ATTACHMENT, indirect=['submitted_workflow'])
    def test_download_feedback_attachment_from_answer(self, submitted_workflow, in_grade_workflow, instructor,
                                                      started_workflow):
        original_file_name = in_grade_workflow['feedback_attachments'][0]['name']
        request_id = instructor['request_id']
        answer_id = submitted_workflow['answers'][0]['answer_id']
        feedback_attachment_id = in_grade_workflow['feedback_attachments'][0]['answer_feedback_attachment_id']

        response = get_feedback_attachment_link_from_answer(request_id, answer_id, feedback_attachment_id)
        download_link = response.json()['url']
        file_path, downloaded_file_name = download_file(download_link)

        self.assert_attr(original_file_name, downloaded_file_name, 'File name')
        self.assert_downloaded_file(downloaded_file_name)
