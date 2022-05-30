import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.resource_libraries.resource_libraries import get_resource_libraries, update_resource_library, \
    delete_resource_library, get_resource_library, get_resource_libraries_query, create_resource_library, \
    get_resource_library_actions, get_resource_library_resources
from models.users.activity import SupportedLTIVersion
from models.users.resource_libraries import SupportedResourceLibraryModel, ResourceLibraries, ResourceLibrariesAction
from parameters.api.users.resource_library import resource_library_methods, RESOURCE_LIBRARIES_LIMIT
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.resource_libraries
@allure.epic('Core LMS')
@allure.feature('Resource libraries')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestResourceLibrariesApi(BaseAPI):
    resource_library = ResourceLibraries.manager
    related_fields = ResourceLibraries.manager.related_fields()
    library_models = SupportedResourceLibraryModel.to_list()
    library_ids = SupportedResourceLibraryModel.to_ids()

    @allure.id("4429")
    @allure.title('Get resource libraries (API)')
    def test_get_resource_libraries(self):
        response = get_resource_libraries()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.resource_library.to_array_schema)

    @allure.id("4440")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1226',
        name='authUrl ignored on POST to /api/v1/resource-libraries'
    )
    @pytest.mark.parametrize('resource_library', library_models, ids=library_ids)
    def test_create_resource_library(self, request, resource_library):
        allure.dynamic.title(f'Create resource library with type "{request.node.callspec.id}" (API)')
        resource_library_payload = resource_library.manager.to_dict()
        response = create_resource_library(resource_library_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_model_equal(json_response, resource_library_payload, resource_library, self.related_fields)
        self.validate_json(json_response, resource_library.manager.to_schema)

    @allure.id("4433")
    @pytest.mark.parametrize('resource_library', library_models, ids=library_ids, indirect=['resource_library'])
    def test_update_resource_library(self, request, resource_library):
        allure.dynamic.title(f'Update resource library with type "{request.node.callspec.id}" (API)')
        library_model, resource_library = resource_library
        resource_library_payload = {**library_model.manager.to_json, 'id': resource_library['id']}

        response = update_resource_library(resource_library['id'], resource_library_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_model_equal(json_response, resource_library_payload, library_model, self.related_fields)
        self.validate_json(json_response, self.resource_library.to_schema)

    @allure.id("4435")
    @allure.title('Delete resource library (API)')
    def test_delete_resource_library(self, resource_library):
        _, resource_library = resource_library
        response = delete_resource_library(resource_library['id'])
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("4439")
    @allure.title('Get resource library (API)')
    def test_get_resource_library(self, resource_library):
        _, resource_library = resource_library
        response = get_resource_library(resource_library['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_json(json_response, resource_library)
        self.validate_json(json_response, self.resource_library.to_schema)

    @allure.id("4430")
    @pytest.mark.parametrize('query',
                             to_sort_query(resource_library.to_json, exclude=resource_library.related_fields()))
    @allure.title('Query resource libraries (API)')
    def test_query_resource_libraries(self, query):
        response = get_resource_libraries_query(query)

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("4431")
    @allure.title('Check authorization for resource libraries endpoints (API)')
    @pytest.mark.parametrize('endpoint', resource_library_methods, ids=to_method_param)
    def test_check_authorization_for_groups_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))

    @allure.id("4583")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1291',
        name='[Administrator][Ztool] 403 errors on /api/v1/actions, /api/v1/elements'
    )
    @allure.title('Get resource libraries actions (API)')
    def test_get_resource_libraries_actions(self, resource_library):
        _, resource_library = resource_library
        response = get_resource_library_actions(resource_library['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, ResourceLibrariesAction.manager.to_array_schema)

    @allure.id("4582")
    @allure.title('Get resource libraries resources for VirtualLab with "ltiVersion=1" (API)')
    def test_get_resource_libraries_resources(self, resource_library_virtual_lab):
        response = get_resource_library_resources(resource_library_virtual_lab['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_all(
            json_response,
            [{'ltiVersion': SupportedLTIVersion.LTI_1_1.value} for _ in range(RESOURCE_LIBRARIES_LIMIT)],
            'resource library',
            ['ltiVersion']
        )
