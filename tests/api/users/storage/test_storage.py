import os

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.storage.storage import delete_from_storage, upload_to_storage, get_from_storage
from settings import RERUNS, RERUNS_DELAY, PROJECT_ROOT
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import get_default_files
from utils.formatters.parametrization import to_method_param
from utils.utils import random_string


@pytest.mark.api
@pytest.mark.storage
@allure.epic('Core LMS')
@allure.feature('Storage')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestStorageApi(BaseAPI):
    files = get_default_files()

    @allure.id("490")
    @pytest.mark.parametrize('file_path', files)
    @allure.title('Upload files to storage (API)')
    def test_upload_files_to_storage(self, file_path):
        files = {'file': open(file_path, 'rb')}
        payload = {'path': f'{random_string()}/'}
        file_name = os.path.basename(file_path)

        response = upload_to_storage(payload=payload, files=files)
        json_response = response.json()

        file_uri = '/api/v1/storage/' + payload['path'] + file_name
        uploaded_file_path = payload['path'] + file_name

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['fileUrl'], file_uri.lower(), 'File url')
        self.assert_attr(json_response['filePath'], uploaded_file_path, 'File path')

    @allure.id("493")
    @pytest.mark.skip(reason='Not handled exception for /api/v1/storage uploading files')
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-242',
        name='Not handled exception for /api/v1/storage uploading files'
    )
    @allure.title('Upload files to storage negative (API)')
    def test_upload_files_to_storage_negative(self):
        files = {'file': None}
        payload = {'path': None}

        response = upload_to_storage(payload=payload, files=files)

        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)

    @allure.id("491")
    @pytest.mark.parametrize('file_path', files)
    @allure.title('Get file from storage (API)')
    def test_get_file_from_storage(self, file_path):
        files = {'file': open(file_path, 'rb')}
        payload = {'path': f'{random_string()}/'}
        file_name = os.path.basename(file_path)

        file_uri = upload_to_storage(payload=payload, files=files).json()['filePath']
        response = get_from_storage(file_uri)

        with open(file_name, 'wb') as storage_file:
            storage_file.write(response.content)

        self.assert_response_status(response.status_code, self.http.OK)
        assert os.path.isfile(file_name)

        os.remove(file_name)

    @allure.id("492")
    @allure.title('Get file from storage negative (API)')
    def test_get_file_from_storage_negative(self):
        response = get_from_storage(random_string() + '/random.png')
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("494")
    @allure.title('Delete file from storage negative (API)')
    def test_delete_file_from_storage_negative(self):
        response = delete_from_storage(random_string() + '/random.png')
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("495")
    @pytest.mark.parametrize('file_path', files)
    @allure.title('Delete file from storage (API)')
    def test_delete_file_from_storage(self, file_path):
        files = {'file': open(file_path, 'rb')}
        payload = {'path': f'{random_string()}/'}
        file_path = upload_to_storage(payload=payload, files=files).json()['filePath']

        response = delete_from_storage(file_path)

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_truth(response.json(), 'Response body')

    @allure.id("912")
    @allure.title('Check authorization for storage endpoints (API)')
    @pytest.mark.parametrize('endpoint', [
        {
            'method': upload_to_storage,
            'args': ({'path': f'{random_string()}/'},
                     {'files': open(PROJECT_ROOT + '/parameters/files/some.png', 'rb')})
        },
        {
            'method': delete_from_storage,
            'args': ('some_file',)
        }
    ], ids=to_method_param)
    def test_check_authorization_for_storage_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
