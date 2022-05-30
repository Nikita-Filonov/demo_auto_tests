from http import HTTPStatus

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.tenants.tenants import update_tenant, create_tenant, get_tenant, get_tenants
from base.api.users.tenants.tenants_checks import is_tenant_created, is_tenant_updated
from models.users.tenant import Tenants, get_default_tenant
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.api.users.permissions import PermissionsStory
from utils.api.users.common import Endpoint
from utils.api.users.permissions import make_methods_payload_for_permissions, check_permissions_for_entity, \
    EXCLUDE_PERMISSIONS_ENDPOINTS
from utils.formatters.parametrization import to_method_param
from utils.utils import cache_callable


@pytest.mark.api
@pytest.mark.permissions
@pytest.mark.permissions_scopes
@allure.epic('Core LMS')
@allure.feature('Permissions')
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_TENANTS.value)
@pytest.mark.parametrize('user_with_permissions_class', [Tenants.SCOPE], indirect=['user_with_permissions_class'])
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForTenantsApi(BaseAPI):
    exclude = ['tenants', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    tenant_id = cache_callable(get_default_tenant)
    tenant_payload = Tenants

    @allure.id("4152")
    @allure.title('Check permissions for "Tenants" model (API)')
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1265', name="Tenants. Admin can't create tenant.")
    @pytest.mark.parametrize('endpoint', [
        {'method': get_tenants, 'args': (), 'response': HTTPStatus.OK},
        {'method': get_tenant, 'args': (tenant_id,), 'response': HTTPStatus.OK},
        {'method': create_tenant, 'args': (tenant_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': update_tenant, 'args': (tenant_id, tenant_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': is_tenant_created, 'args': (tenant_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_tenant_updated, 'args': (tenant_id,), 'response': HTTPStatus.NOT_FOUND},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_tenants_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
