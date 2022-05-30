import uuid

import allure
import pytest
from alms_integration import create_oauth1_credentials

from base.api.base import BaseAPI
from base.api.users.oauth1_credentials.oauth1_credentials import get_oauth1_credentials, update_oauth1_credential, \
    get_oauth1_credential, get_oauth1_credentials_query
from models.users.oauth1_credentials import Oauth1Credentials
from parameters.api.users.oauth1_credentials import oauth1_credential_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.oauth1_credentials
@allure.epic('Core LMS')
@allure.feature('Oauth1 credentials')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestOauth1CredentialsApi(BaseAPI):
    oauth1_credentials = Oauth1Credentials.manager

    @allure.id("527")
    @allure.title('Get oauth1 credentials (API)')
    def test_get_oauth1_credentials(self):
        response = get_oauth1_credentials()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.oauth1_credentials.to_array_schema)

    @allure.id("530")
    @allure.title('Create oauth1 credential (API)')
    def test_create_oauth1_credential(self):
        oauth1_credentials_payload = self.oauth1_credentials.to_json

        response = create_oauth1_credentials(oauth1_credentials_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], oauth1_credentials_payload['id'],
                         Oauth1Credentials.o_auth1credential_id.json)
        self.assert_attr(json_response['url'], oauth1_credentials_payload['url'], Oauth1Credentials.url.json)
        self.assert_attr(json_response['consumerKey'], oauth1_credentials_payload['consumerKey'],
                         Oauth1Credentials.consumer_key.json)
        self.assert_attr(json_response['secretKey'], oauth1_credentials_payload['secretKey'],
                         Oauth1Credentials.secret_key.json)
        self.validate_json(json_response, self.oauth1_credentials.to_schema)

    @allure.id("528")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-524',
        name='Unable to update OAuth1 credentials'
    )
    @allure.title('Update oauth1 credentials (API)')
    def test_update_oauth1_credentials(self, oauth1_credentials):
        oauth1_credentials_payload = self.oauth1_credentials.to_json

        response = update_oauth1_credential(oauth1_credentials['id'], oauth1_credentials_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], oauth1_credentials['id'], Oauth1Credentials.o_auth1credential_id.json)
        self.assert_attr(json_response['url'], oauth1_credentials_payload['url'], Oauth1Credentials.url.json)
        self.assert_attr(json_response['consumerKey'], oauth1_credentials_payload['consumerKey'],
                         Oauth1Credentials.consumer_key.json)
        self.assert_attr(json_response['secretKey'], oauth1_credentials_payload['secretKey'],
                         Oauth1Credentials.secret_key.json)
        self.validate_json(json_response, self.oauth1_credentials.to_schema)

    @allure.id("4509")
    @pytest.mark.xfail(reason='Validations errors')
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1220', name='Validations errors')
    @allure.title('Update oauth1 credentials negative (API)')
    def test_update_oauth1_credentials_negative(self, oauth1_credentials):
        oauth1_credentials_payload = self.oauth1_credentials.to_negative_json()

        response = update_oauth1_credential(oauth1_credentials['id'], oauth1_credentials_payload)
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)

    @allure.id("532")
    @allure.title('Get oauth1 credential (API)')
    def test_get_oauth1_credential(self, oauth1_credentials):
        response = get_oauth1_credential(oauth1_credentials['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_json(json_response, oauth1_credentials)
        self.validate_json(json_response, self.oauth1_credentials.to_schema)

    @allure.id("533")
    @allure.title('Get oauth1 credential negative (API)')
    def test_get_role_pattern_permission_negative(self):
        response = get_oauth1_credential(uuid.uuid4())
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("1887")
    @pytest.mark.parametrize('query', to_sort_query(oauth1_credentials.to_json,
                                                    exclude=oauth1_credentials.related_fields()))
    @allure.title('Query oauth1 credentials (API)')
    def test_query_oauth1_credentials(self, query):
        response = get_oauth1_credentials_query(query)

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("916")
    @allure.title('Check authorization for oauth1 credentials endpoints (API)')
    @pytest.mark.parametrize('endpoint', oauth1_credential_methods, ids=to_method_param)
    def test_check_authorization_for_oauth1_credentials_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
