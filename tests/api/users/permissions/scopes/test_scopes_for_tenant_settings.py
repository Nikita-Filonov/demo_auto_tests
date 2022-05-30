from http import HTTPStatus

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.tenant_settings.tenant_settings import get_tenant_setting, get_tenant_settings, \
    create_tenant_setting, update_tenant_setting, delete_tenant_setting
from base.api.users.tenant_settings.tenant_settings_checks import is_tenant_setting_created, is_tenant_setting_updated, \
    is_tenant_setting_deleted
from models.users.tenant_setting import get_default_tenant_setting, TenantSettings
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.api.users.permissions import PermissionsStory
from utils.api.users.common import Endpoint
from utils.api.users.permissions import make_methods_payload_for_permissions, check_permissions_for_entity
from utils.formatters.parametrization import to_method_param
from utils.utils import cache_callable


@pytest.mark.api
@pytest.mark.permissions
@pytest.mark.permissions_scopes
@allure.epic('Core LMS')
@allure.feature('Permissions')
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_TENANT_SETTINGS.value)
@pytest.mark.parametrize(
    'user_with_permissions_class',
    [TenantSettings.SCOPE],
    indirect=['user_with_permissions_class']
)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForTenantSettingsApi(BaseAPI):
    exclude = ['tenant_settings']
    tenant_setting_id = cache_callable(get_default_tenant_setting)
    tenant_setting_payload = TenantSettings

    @allure.id("4386")
    @allure.title('Check permissions for "TenantSettings" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_tenant_setting, 'args': (tenant_setting_id,), 'response': HTTPStatus.OK},
        {'method': get_tenant_settings, 'args': (), 'response': HTTPStatus.OK},
        {'method': create_tenant_setting, 'args': (tenant_setting_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': update_tenant_setting, 'args': (tenant_setting_id, TenantSettings.manager.to_json),
         'response': HTTPStatus.ACCEPTED},
        {'method': delete_tenant_setting, 'args': (tenant_setting_id,), 'response': HTTPStatus.ACCEPTED},
        {'method': is_tenant_setting_created, 'args': (tenant_setting_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_tenant_setting_updated, 'args': (tenant_setting_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_tenant_setting_deleted, 'args': (tenant_setting_id,), 'response': HTTPStatus.NOT_FOUND},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_tenant_settings_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
