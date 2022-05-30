from base.api.users.tenant_settings.tenant_settings import get_tenant_settings, update_tenant_setting
from parameters.api.users.tenant_settings import default_tenant_settings
from utils.utils import find


def reset_tenant_settings():
    """
    Set default Tenant Settings for default user with default names and values

    Get current tenant settings,
    find tenant setting by default setting name and get current tenant setting properties,
    compare tenant setting value in dictionary with default tenant setting value,
    compare result: the same - continue
    compare result: different - update/put default tenant setting in DB by API
    """
    current_tenant_settings = get_tenant_settings().json()
    for setting_name, setting_value in default_tenant_settings:
        tenant_setting = find(lambda ts: ts['name'] == setting_name, current_tenant_settings)

        if tenant_setting['value'] == setting_value:
            continue

        update_tenant_setting(tenant_setting['id'], {**tenant_setting, 'value': setting_value})
