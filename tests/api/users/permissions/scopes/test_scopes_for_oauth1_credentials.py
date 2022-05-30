from http import HTTPStatus

import allure
import pytest
from alms_integration import create_oauth1_credentials

from base.api.base import BaseAPI
from base.api.users.oauth1_credentials.oauth1_credentials import get_oauth1_credentials, update_oauth1_credential, \
    get_oauth1_credential
from base.api.users.oauth1_credentials.oauth1_credentials_checks import is_oauth1_credential_created, \
    is_oauth1_credential_updated
from models.users.oauth1_credentials import Oauth1Credentials, get_default_oauth1_credentials
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.api.users.permissions import PermissionsStory
from utils.api.users.common import Endpoint
from utils.api.users.permissions import make_methods_payload_for_permissions, \
    EXCLUDE_PERMISSIONS_ENDPOINTS, check_permissions_for_entity
from utils.formatters.parametrization import to_method_param
from utils.utils import cache_callable


@pytest.mark.api
@pytest.mark.permissions
@pytest.mark.permissions_scopes
@allure.epic('Core LMS')
@allure.feature('Permissions')
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_OAUTH1_CREDENTIALS.value)
@pytest.mark.parametrize(
    'user_with_permissions_class',
    [Oauth1Credentials.SCOPE],
    indirect=['user_with_permissions_class']
)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForOAuth1CredentialsApi(BaseAPI):
    exclude = ['oauth1_credentials', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    oauth1_credential_id = cache_callable(get_default_oauth1_credentials)
    oauth1_credential_payload = Oauth1Credentials

    @allure.id("1828")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-524',
        name='Unable to update OAuth1 credentials'
    )
    @allure.title('Check permissions for "Oauth1Credentials" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_oauth1_credentials, 'args': (), 'response': HTTPStatus.OK},
        {'method': get_oauth1_credential, 'args': (oauth1_credential_id,), 'response': HTTPStatus.OK},
        {'method': create_oauth1_credentials, 'args': (oauth1_credential_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': update_oauth1_credential, 'args': (oauth1_credential_id, oauth1_credential_payload,),
         'response': HTTPStatus.ACCEPTED},
        {'method': is_oauth1_credential_created, 'args': (oauth1_credential_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_oauth1_credential_updated, 'args': (oauth1_credential_id,), 'response': HTTPStatus.NOT_FOUND},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_oauth1_credentials_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
