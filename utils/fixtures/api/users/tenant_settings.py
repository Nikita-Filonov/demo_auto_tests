import allure
import pytest

from base.api.users.tenant_settings.tenant_settings import update_tenant_setting, get_tenant_setting, \
    create_tenant_setting
from models.users.tenant_setting import TenantSettings


@pytest.fixture(scope='function')
def update_tenant_setting_value(request):
    """
    Uses to update value for tenant setting with custom tenant setting

    Example:
         update_tenant_setting_value({key: 'platform.common.locale', value: 'ru-RU'})
         -> default value (EN) update to custom value (RU)
    """
    if not hasattr(request, 'param'):
        pytest.fail('Fixture "update_tenant_setting_value" requires param')

    tenant_setting_key, tenant_setting_value = request.param.values()

    with allure.step(f'Admin update "{tenant_setting_key}" tenant setting with value: "{tenant_setting_value}"'):
        tenant_setting = get_tenant_setting(tenant_setting_id=tenant_setting_key).json()
        update_tenant_setting(tenant_setting['id'], {**tenant_setting, 'value': tenant_setting_value})


@pytest.fixture(scope='function')
def tenant_setting_function():
    payload = TenantSettings.manager.to_json
    return create_tenant_setting(payload).json()


@pytest.fixture(scope='class')
def tenant_setting_class():
    payload = TenantSettings.manager.to_json
    return create_tenant_setting(payload).json()
