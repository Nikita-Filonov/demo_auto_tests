import allure
import pytest

from base.api.base import BaseAPI
from base.api.ztool.element import upload_file_to_element, get_element_files, delete_file_from_element, \
    update_file_in_element
from models.ztool.element import ElementFiles
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.api.ztool.elements import ElementsStory
from utils.api.utils import COMMON_FILES
from utils.api.ztool.elements import get_element_file_url
from utils.utils import file_name_or_path_resolve


@allure.issue(
    url='https://youtrack.alemira.dev/issue/ALMS-1107',
    name='204 response code on GET to /api/v1/objectives/{id}/objective-workflow-aggregate'
)
@pytest.mark.api
@pytest.mark.element_files
@allure.epic('Core LMS')
@allure.feature('Elements')
@allure.story(ElementsStory.ELEMENT_FILES.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestElementFilesApi(BaseAPI):
    file = file_name_or_path_resolve(COMMON_FILES[0])
    element_files = ElementFiles.manager
    NUMBER_OF_FILES = len(COMMON_FILES)

    @allure.id("4246")
    @allure.title('Upload file to element (API)')
    @pytest.mark.parametrize('file_path', COMMON_FILES)
    def test_upload_file_to_element(self, author, file_path):
        upload_response = upload_file_to_element(author['request_id'], author['element_id'], file_path)

        response = get_element_files(author['request_id'], author['element_id'])
        file_name, file_url = response.json()[0].values()

        expected_file_name, expected_url = get_element_file_url(author["element_id"], file_path)

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_response_status(upload_response.status_code, self.http.NO_CONTENT)
        self.assert_attr(file_name, expected_file_name, ElementFiles.name.json)
        self.assert_attr(file_url, expected_url, ElementFiles.url.json)

    @allure.id("4245")
    @allure.title('Upload file to element that already exists in storage (API)')
    @pytest.mark.parametrize('file_path', COMMON_FILES)
    @pytest.mark.parametrize('author', [{'files': COMMON_FILES}], indirect=['author'])
    def test_upload_file_to_element_that_already_exists_in_storage(self, author, file_path):
        upload_response = upload_file_to_element(author['request_id'], author['element_id'], file_path)

        response = get_element_files(author['request_id'], author['element_id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_response_status(upload_response.status_code, self.http.NO_CONTENT)
        self.assert_attr(len(json_response), self.NUMBER_OF_FILES, 'Number of files')
        self.validate_json(json_response, self.element_files.to_array_schema)

    @allure.id("4236")
    @allure.title('Get element files (API)')
    @pytest.mark.parametrize('author', [{'files': COMMON_FILES}], indirect=['author'])
    def test_get_element_files(self, author):
        response = get_element_files(author['request_id'], author['element_id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(len(json_response), self.NUMBER_OF_FILES, 'Number of files')
        self.validate_json(json_response, self.element_files.to_array_schema)

    @allure.id("4244")
    @allure.title('Delete file from the element (API)')
    @pytest.mark.parametrize('author', [{'files': COMMON_FILES}], indirect=['author'])
    def test_delete_file_from_the_element(self, author):
        delete_response = delete_file_from_element(author['request_id'], author['element_id'], self.file)

        response = get_element_files(author['request_id'], author['element_id'])
        json_response = response.json()

        safe_number_of_files = len([file for file in json_response if file[ElementFiles.name.json] != self.file])

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_response_status(delete_response.status_code, self.http.NO_CONTENT)
        self.assert_attr(len(json_response), safe_number_of_files, 'Number of files')

    @allure.id("4237")
    @allure.title('Update file in the element (API)')
    @pytest.mark.parametrize('author', [{'files': COMMON_FILES}], indirect=['author'])
    def test_update_file_in_the_element(self, author):
        payload = self.element_files.to_json
        update_response = update_file_in_element(author['request_id'], author['element_id'], self.file, payload)

        response = get_element_files(author['request_id'], author['element_id'])
        file_name, file_url = response.json()[0].values()

        _, expected_url = get_element_file_url(author["element_id"], payload[ElementFiles.name.json])

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_response_status(update_response.status_code, self.http.NO_CONTENT)
        self.assert_attr(file_name, payload[ElementFiles.name.json], ElementFiles.name.json)
        self.assert_attr(file_url, expected_url, ElementFiles.url.json)
