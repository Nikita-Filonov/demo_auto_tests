import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.resource_libraries.file_resource_libraries.directories import move_resource_library_directory, \
    delete_resource_library_directory, create_resource_library_directory
from base.api.users.resource_libraries.file_resource_libraries.files import upload_resource_library_file, \
    delete_resource_library_file, move_resource_library_file, get_resource_library_file_download_link
from models.users.resource_libraries import ResourceLibrariesPrivateFile
from models.users.resource_library_files import ResourceLibraryFileJsonPayload, RecourseLibraryDownloadFile
from settings import RERUNS, RERUNS_DELAY
from tests.api.ztool.conftest import EXCLUDE_FILES
from utils.api.utils import get_default_files
from utils.assertions.resource_libraries import ensure_user_can_view_file, ensure_user_can_view_directory, \
    ensure_user_can_not_view_directory
from utils.minio.utils import switch_file_name, safe_storage_path
from utils.utils import random_string


@pytest.mark.api
@pytest.mark.file_resource_libraries
@allure.epic('Core LMS')
@allure.feature('File resource libraries')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(url='https://youtrack.alemira.dev/issue/ALMS-1278', name='File resource library')
@allure.issue(
    url='https://youtrack.alemira.dev/issue/ALMS-1372',
    name='GET api/v1/resource-libraries/{libraryId}/resources/{RecoursePath} does not work'
)
@pytest.mark.parametrize('resource_library', [ResourceLibrariesPrivateFile], indirect=['resource_library'])
class TestFileResourceLibrariesApi(BaseAPI):
    files = get_default_files(EXCLUDE_FILES)
    default_file = files[0]

    @allure.id("5321")
    @allure.title('Create file for resource library (API)')
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1427',
        name='[File resource library] Wrong file type detecting for *.odt, *.odp'
    )
    @pytest.mark.parametrize('local_file', files)
    def test_create_file_for_resource_library(self, resource_library, local_file):
        _, resource_library = resource_library

        storage_path = switch_file_name(local_file, new_path=f'/{random_string()}/')
        response = upload_resource_library_file(
            resource_library_id=resource_library['id'],
            storage_path=storage_path,
            local_file=local_file,
        )

        self.assert_response_status(response.status_code, self.http.NO_CONTENT)
        self.assert_file_exists_in_bucket_folder(storage_path)
        ensure_user_can_view_file(resource_library['id'], storage_path, local_file)
        ensure_user_can_view_directory(resource_library['id'], storage_path)

    @allure.id("5324")
    @allure.title('Delete file from resource library (API)')
    @pytest.mark.parametrize(
        'resource_library_with_file',
        [
            {
                'local_file': default_file,
                'storage_path': switch_file_name(default_file, new_path=f'/{random_string()}/'),
            }
        ],
        indirect=['resource_library_with_file']
    )
    def test_delete_file_from_recourse_library(self, resource_library, resource_library_with_file):
        _, resource_library = resource_library
        storage_path = resource_library_with_file['storage_path']
        response = delete_resource_library_file(resource_library['id'], storage_path)

        self.assert_response_status(response.status_code, self.http.NO_CONTENT)
        self.assert_file_does_not_exists_in_bucket_folder(storage_path)

    @allure.id("5327")
    @allure.title('Move recourse library file (API)')
    @pytest.mark.parametrize(
        'resource_library_with_file',
        [
            {
                'local_file': default_file,
                'storage_path': switch_file_name(default_file, new_path=f'/{random_string()}/'),
            }
        ],
        indirect=['resource_library_with_file']
    )
    def test_move_recourse_library_file(self, resource_library, resource_library_with_file):
        _, resource_library = resource_library
        from_path, local_file = resource_library_with_file['storage_path'], resource_library_with_file['local_file']
        to_path = switch_file_name(from_path, new_path=f'/{random_string()}/{random_string()}/')

        response = move_resource_library_file(
            resource_library_id=resource_library['id'],
            storage_path=from_path,
            json_payload=ResourceLibraryFileJsonPayload(targetPath=to_path),
        )

        self.assert_response_status(response.status_code, self.http.NO_CONTENT)
        self.assert_file_exists_in_bucket_folder(to_path)
        self.assert_file_does_not_exists_in_bucket_folder(from_path)
        ensure_user_can_view_file(resource_library['id'], to_path, local_file)
        ensure_user_can_view_directory(resource_library['id'], to_path)

    @allure.id("5322")
    @allure.title('Move recourse library directory (API)')
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1426',
        name='[File resource library] Unable to move directory'
    )
    @pytest.mark.parametrize(
        'resource_library_with_directory',
        [{'file_name_or_path': f'/{random_string()}/'}],
        indirect=['resource_library_with_directory']
    )
    def test_move_recourse_library_directory(self, resource_library_with_directory):
        from_directory, resource_library = resource_library_with_directory
        to_directory = switch_file_name(from_directory, new_path=f'/{random_string()}/')

        response = move_resource_library_directory(
            resource_library_id=resource_library['id'],
            storage_path=from_directory,
            json_payload=ResourceLibraryFileJsonPayload(targetPath=to_directory)
        )

        self.assert_response_status(response.status_code, self.http.NO_CONTENT)
        ensure_user_can_view_directory(resource_library['id'], to_directory)
        ensure_user_can_not_view_directory(resource_library['id'], from_directory)

    @allure.id("5326")
    @allure.title('Create directory for resource library (API)')
    def test_create_directory_for_resource_library(self, resource_library):
        _, resource_library = resource_library

        directory = safe_storage_path(file_name_or_path=f'/{random_string()}/')
        response = create_resource_library_directory(resource_library['id'], directory)
        self.assert_response_status(response.status_code, self.http.NO_CONTENT)
        ensure_user_can_view_directory(resource_library['id'], directory)

    @allure.id("5325")
    @allure.title('Delete directory from recourse library (API)')
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1425',
        name='[File resource library] Unable to delete directory'
    )
    @pytest.mark.parametrize(
        'resource_library_with_directory',
        [{'file_name_or_path': f'/{random_string()}/'}],
        indirect=['resource_library_with_directory']
    )
    def test_delete_directory_from_recourse_library(self, resource_library_with_directory):
        directory, resource_library = resource_library_with_directory

        response = delete_resource_library_directory(resource_library['id'], directory)
        self.assert_response_status(response.status_code, self.http.NO_CONTENT)

    @allure.id("5323")
    @allure.title('Get recourse library download link (API)')
    @pytest.mark.parametrize(
        'resource_library_with_file',
        [
            {
                'local_file': default_file,
                'storage_path': switch_file_name(default_file, new_path=f'/{random_string()}/'),
            }
        ],
        indirect=['resource_library_with_file']
    )
    def test_get_recourse_library_download_link(self, resource_library, resource_library_with_file):
        _, resource_library = resource_library
        storage_path = resource_library_with_file['storage_path']

        response = get_resource_library_file_download_link(resource_library['id'], storage_path)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, RecourseLibraryDownloadFile.manager.to_schema)
