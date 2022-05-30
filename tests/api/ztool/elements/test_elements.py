import allure
import pytest

from base.api.base import BaseAPI
from base.api.ztool.element import get_element, update_element, delete_element, get_grades_of_element, \
    get_exercises_of_element, upload_textbook_attachment_to_element, update_textbook_attachment_in_element, \
    delete_textbook_attachment_from_element, update_grade_in_element
from base.api.ztool.launch import get_launch
from models.users.role import SupportedRoles
from models.ztool.attachment import ElementTextbookAttachments
from models.ztool.element import Elements, Grades, to_element_update_json
from models.ztool.exercise import Exercises
from parameters.courses.ui.ztool.grades import grade_properties
from settings import RERUNS, RERUNS_DELAY, PROJECT_ROOT
from tests.api.ztool.conftest import ROLES
from utils.api.utils import download_file
from utils.api.ztool.permissions import permission_error


@allure.issue(
    url='https://youtrack.alemira.dev/issue/ALMS-1107',
    name='204 response code on GET to /api/v1/objectives/{id}/objective-workflow-aggregate'
)
@pytest.mark.api
@pytest.mark.elements
@allure.epic('Core LMS')
@allure.feature('Elements')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestElementsApi(BaseAPI):
    element = Elements.manager
    grade = Grades.manager
    exercise = Exercises.manager
    attachment = ElementTextbookAttachments.manager

    ROLES_HAS_NO_PERMISSIONS = [SupportedRoles.LEARNER, SupportedRoles.INSTRUCTOR]

    ROLES_CAN_SEE_ANSWER = [SupportedRoles.AUTHOR, SupportedRoles.INSTRUCTOR]
    ROLES_CAN_NOT_SEE_ANSWER = [SupportedRoles.LEARNER]

    ROLES_CAN_UPLOAD_TEXTBOOK_ATTACHMENT = [SupportedRoles.AUTHOR]
    ROLES_CAN_NOT_UPLOAD_TEXTBOOK_ATTACHMENT = [SupportedRoles.LEARNER, SupportedRoles.INSTRUCTOR]

    TEXTBOOKS = [PROJECT_ROOT + '/parameters/files/some.pdf']

    @allure.id("3850")
    @allure.title('Get element (API)')
    @pytest.mark.parametrize('launch', ROLES, indirect=['launch'])
    def test_get_element(self, launch):
        element_payload = self.element.get(element_id=launch['element_id'])
        response = get_element(launch['request_id'], launch['element_id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], element_payload['element_id'], Elements.element_id.json)
        self.assert_attr(json_response['name'], element_payload['name'], Elements.name.json)
        self.assert_attr(json_response['imageUrl'], element_payload['image_url'], Elements.image_url.json)
        self.assert_attr(json_response['textbook'], element_payload['textbook'], Elements.textbook.json)
        self.assert_attr(json_response['minBonus'], element_payload['min_bonus'], Elements.min_bonus.json)
        self.assert_attr(json_response['maxBonus'], element_payload['max_bonus'], Elements.max_bonus.json)
        self.assert_attr(json_response['tutorGuideline'], element_payload['tutor_guideline'],
                         Elements.tutor_guideline.json)
        self.validate_json(json_response, self.element.to_schema)

    @pytest.mark.xfail(
        reason='Objectives: Ztool: 500 error appears after clicking "Update" button (all data are saved)'
    )
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-944',
        name='Objectives: Ztool: 500 error appears after clicking "Update" button (all data are saved)'
    )
    @allure.id("3849")
    @allure.title('Update element (API)')
    def test_update_element(self, author):
        element_payload = to_element_update_json()
        response = update_element(author['request_id'], author['element_id'], element_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], author['element_id'], Elements.element_id.json)
        self.assert_attr(json_response['name'], element_payload['name'], Elements.name.json)
        self.assert_attr(json_response['imageUrl'], element_payload['imageUrl'], Elements.image_url.json)
        self.assert_attr(json_response['textbook'], element_payload['textbook'], Elements.textbook.json)
        self.assert_attr(json_response['minBonus'], element_payload['minBonus'], Elements.min_bonus.json)
        self.assert_attr(json_response['maxBonus'], element_payload['maxBonus'], Elements.max_bonus.json)
        self.assert_attr(json_response['tutorGuideline'], element_payload['tutorGuideline'],
                         Elements.tutor_guideline.json)
        self.validate_json(json_response, self.element.to_schema)

    @allure.id("3851")
    @allure.title('Update element without permissions (API)')
    @pytest.mark.parametrize('launch', ROLES_HAS_NO_PERMISSIONS, indirect=['launch'])
    def test_update_element_without_permissions(self, launch: dict):
        element_payload = to_element_update_json()
        response = update_element(launch['request_id'], launch['element_id'], element_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.FORBIDDEN)
        self.assert_json(json_response, permission_error('Update'))

    @allure.id("3854")
    @allure.title('Delete element (API)')
    @pytest.mark.parametrize('launch', [SupportedRoles.AUTHOR], indirect=['launch'])
    def test_delete_element(self, launch: dict):
        response = delete_element(launch['request_id'], launch['element_id'])
        self.assert_response_status(response.status_code, self.http.OK)

    @allure.id("3852")
    @allure.title('Delete element without permissions (API)')
    @pytest.mark.parametrize('launch', ROLES_HAS_NO_PERMISSIONS, indirect=['launch'])
    def test_delete_element_without_permissions(self, launch: dict):
        response = delete_element(launch['request_id'], launch['element_id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.FORBIDDEN)
        self.assert_json(json_response, permission_error('Delete'))

    @allure.id("3853")
    @allure.title('Get grades of element (API)')
    @pytest.mark.parametrize('launch', ROLES, indirect=['launch'])
    def test_get_grades_of_element(self, launch):
        response = get_grades_of_element(launch['request_id'], launch['element_id'])
        json_response = response.json()
        grades = Grades.manager.filter(element_id=launch['element_id'])

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(len(json_response), len(grade_properties), 'Grades count')
        self.validate_json(json_response, self.grade.to_array_schema)
        for index, grade in enumerate(json_response):
            self.assert_attr(grade['id'], grades[index]['grade_id'], Grades.grade_id.json)
            self.assert_attr(grade['name'], grades[index]['name'], Grades.name.json)
            self.assert_attr(grade['max'], int(grades[index]['max']), Grades.max.json)

    @allure.title('Update grade of element (API)')
    @pytest.mark.parametrize('launch', ROLES_CAN_UPLOAD_TEXTBOOK_ATTACHMENT, indirect=['launch'])
    def test_update_grade_of_element(self, launch: dict):
        grade_payload = self.grade.to_json
        grade = Grades.manager.filter(element_id=launch['element_id'])[0]
        response = update_grade_in_element(launch['request_id'], launch['element_id'], grade['grade_id'], grade_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(grade['grade_id'], json_response['id'], Grades.grade_id.json)
        self.assert_attr(grade_payload['name'], json_response['name'], Grades.name.json)
        self.assert_attr(grade_payload['max'], json_response['max'], Grades.max.json)
        self.validate_json(json_response, self.grade.to_schema)

    @allure.title('Update grade of element negative (API)')
    @pytest.mark.parametrize('launch', ROLES_CAN_NOT_UPLOAD_TEXTBOOK_ATTACHMENT, indirect=['launch'])
    def test_update_grade_of_element_negative(self, launch: dict):
        grade_payload = self.grade.to_json
        grade = Grades.manager.filter(element_id=launch['element_id'])[0]
        response = update_grade_in_element(launch['request_id'], launch['element_id'], grade['grade_id'], grade_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.FORBIDDEN)
        self.assert_json(json_response, permission_error('Update'))

    @allure.id("3859")
    @allure.title('Get exercises of element (API)')
    @pytest.mark.parametrize('launch', ROLES, indirect=['launch'])
    def test_get_exercises_of_element(self, launch, element_with_exercises):
        response = get_exercises_of_element(element_with_exercises['request_id'], element_with_exercises['element_id'])
        json_response = response.json()

        actual_exercise = json_response[0]
        expected_exercise = element_with_exercises['data'][0]

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(len(json_response), len(element_with_exercises['data']), 'Exercises count')
        self.assert_attr(actual_exercise['id'], expected_exercise['exercise_id'], Exercises.exercise_id.json)
        self.assert_attr(actual_exercise['elementId'], expected_exercise['element_id'], Exercises.element_id.json)
        self.assert_attr(actual_exercise['maxScore'], int(expected_exercise['max_score']), Exercises.max_score.json)
        self.assert_attr(actual_exercise['slug'], expected_exercise['slug'], Exercises.slug.json)
        self.assert_attr(actual_exercise['text'], expected_exercise['text'], Exercises.text.json)
        self.assert_attr(actual_exercise['group'], expected_exercise['group'], Exercises.group.json)
        self.assert_attr(actual_exercise['order'], expected_exercise['order'], Exercises.order.json)

        if element_with_exercises['role'] in self.ROLES_CAN_NOT_SEE_ANSWER:
            self.assert_attr(actual_exercise['correctAnswer'], None, Exercises.correct_answer.json)
            self.assert_attr(actual_exercise['tutorGuideline'], None, Exercises.tutor_guideline.json)

        if element_with_exercises['role'] in self.ROLES_CAN_SEE_ANSWER:
            self.assert_attr(actual_exercise['correctAnswer'], expected_exercise['correct_answer'],
                             Exercises.correct_answer.json)
            self.assert_attr(actual_exercise['tutorGuideline'], expected_exercise['tutor_guideline'],
                             Exercises.tutor_guideline.json)
        self.validate_json(actual_exercise, self.exercise.to_schema)

    @allure.id("3855")
    @allure.title('Upload textbook attachment to the element (API)')
    @pytest.mark.parametrize('file_path', TEXTBOOKS)
    @pytest.mark.parametrize('launch', ROLES_CAN_UPLOAD_TEXTBOOK_ATTACHMENT, indirect=['launch'])
    def test_upload_textbook_attachments_to_the_element(self, file_path, launch: dict):
        textbook_payload = ElementTextbookAttachments.manager.to_json
        file_response = upload_textbook_attachment_to_element(launch['request_id'], launch['element_id'],
                                                              textbook_payload)

        element_response = get_element(launch['request_id'], launch['element_id'])
        textbook_attachment = element_response.json()['textbookAttachments'][0]

        self.assert_response_status(file_response.status_code, self.http.OK)
        self.assert_response_status(element_response.status_code, self.http.OK)
        self.assert_attr(textbook_attachment['name'], textbook_payload['name'], 'Textbook attachment file name')
        self.assert_attr(textbook_attachment['url'], textbook_payload['url'], 'Textbook attachment file url')

    @allure.id("3855")
    @allure.title('Upload textbook attachment to the element negative (API)')
    @pytest.mark.parametrize('file_path', TEXTBOOKS)
    @pytest.mark.parametrize('launch', ROLES_CAN_NOT_UPLOAD_TEXTBOOK_ATTACHMENT, indirect=['launch'])
    def test_upload_textbook_attachments_to_the_element_negative(self, file_path, launch: dict):
        textbook_payload = ElementTextbookAttachments.manager.to_json
        response = upload_textbook_attachment_to_element(launch['request_id'], launch['element_id'], textbook_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.FORBIDDEN)
        self.assert_json(json_response, permission_error('Update'))

    @allure.id("3860")
    @allure.title('Update textbook attachment inside the element (API)')
    @pytest.mark.parametrize('launch', ROLES_CAN_UPLOAD_TEXTBOOK_ATTACHMENT, indirect=['launch'])
    def test_update_textbook_attachment_inside_the_element(self, launch: dict, element_with_textbook_attachment):
        textbook_attachment = element_with_textbook_attachment['data']['textbookAttachments'][0]
        request_id = launch['request_id']
        element_id = launch['element_id']

        attachment_payload = self.attachment.to_json
        attachment_response = update_textbook_attachment_in_element(request_id,
                                                                    element_id,
                                                                    textbook_attachment['id'],
                                                                    attachment_payload)
        element_response = get_element(request_id, element_id)
        element_json_response = element_response.json()
        attachment = element_json_response['textbookAttachments'][0]

        self.assert_response_status(element_response.status_code, self.http.OK)
        self.assert_response_status(attachment_response.status_code, self.http.OK)
        self.assert_attr(element_json_response['id'], element_id, Elements.element_id.json)
        self.assert_attr(attachment['id'], textbook_attachment['id'],
                         ElementTextbookAttachments.element_textbook_attachment_id.json)
        self.assert_attr(attachment['name'], attachment_payload['name'], ElementTextbookAttachments.name.json)
        self.validate_json(element_json_response, self.element.to_schema)

    @allure.id("3858")
    @allure.title('Update textbook attachment inside the element negative (API)')
    @pytest.mark.parametrize('launch', ROLES_CAN_UPLOAD_TEXTBOOK_ATTACHMENT, indirect=['launch'])
    @pytest.mark.parametrize('role', ROLES_CAN_NOT_UPLOAD_TEXTBOOK_ATTACHMENT)
    def test_update_textbook_attachment_inside_the_element_negative(self,
                                                                    role,
                                                                    launch: dict,
                                                                    element_with_textbook_attachment):
        element_id = launch['element_id']
        role_launch = get_launch(role, element_id, launch['workflow_id'], launch['objective_id'])
        request_id = role_launch['request_id']
        attachment_id = element_with_textbook_attachment['data']['textbookAttachments'][0]['id']

        payload = self.attachment.to_json
        response = update_textbook_attachment_in_element(request_id, element_id, attachment_id, payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.FORBIDDEN)
        self.assert_json(json_response, permission_error('Update'))

    @allure.id("3856")
    @allure.title('Delete textbook attachment from the element (API)')
    @pytest.mark.parametrize('launch', ROLES_CAN_UPLOAD_TEXTBOOK_ATTACHMENT, indirect=['launch'])
    def test_delete_textbook_attachment_from_the_element(self, launch: dict, element_with_textbook_attachment):
        request_id = launch['request_id']
        element_id = launch['element_id']
        attachment_id = element_with_textbook_attachment['data']['textbookAttachments'][0]['id']

        delete_response = delete_textbook_attachment_from_element(request_id, element_id, attachment_id)

        element_response = get_element(request_id, element_id)
        textbook_attachments = element_response.json()['textbookAttachments']

        self.assert_response_status(delete_response.status_code, self.http.OK)
        self.assert_response_status(element_response.status_code, self.http.OK)
        self.assert_attr(textbook_attachments, [], 'Textbook attachments')

    @allure.id("3861")
    @allure.title('Delete textbook attachment from the element negative (API)')
    @pytest.mark.parametrize('launch', ROLES_CAN_UPLOAD_TEXTBOOK_ATTACHMENT, indirect=['launch'])
    @pytest.mark.parametrize('role', ROLES_CAN_NOT_UPLOAD_TEXTBOOK_ATTACHMENT)
    def test_download_textbook_attachment_from_the_element_negative(
            self, role, launch: dict, element_with_textbook_attachment):
        element_id = launch['element_id']
        role_launch = get_launch(role, element_id, launch['workflow_id'], launch['objective_id'])
        request_id = role_launch['request_id']
        attachment_id = element_with_textbook_attachment['data']['textbookAttachments'][0]['id']

        response = delete_textbook_attachment_from_element(request_id, element_id, attachment_id)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.FORBIDDEN)
        self.assert_json(json_response, permission_error('Update'))

    @allure.id("3857")
    @allure.title('Download textbook attachment from the element (API)')
    @pytest.mark.parametrize('launch', ROLES_CAN_UPLOAD_TEXTBOOK_ATTACHMENT, indirect=['launch'])
    def test_download_textbook_attachment_from_the_element(self, launch: dict, element_with_textbook_attachment):
        textbook_attachment_url = element_with_textbook_attachment['data']['textbookAttachments'][0]['url']

        file_path, downloaded_file_name = download_file(textbook_attachment_url)
        self.assert_downloaded_file(downloaded_file_name)
