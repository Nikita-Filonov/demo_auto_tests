import pytest

from base.ui.administrator.tenant_settings.tenant_settings_page import AdministratorTenantSettingPage
from base.ui.login_page import LoginPage, UsersViews


@pytest.fixture(scope='function')
def tenant_settings_page(py) -> AdministratorTenantSettingPage:
    login_page = LoginPage(py=py, view=UsersViews.ADMINISTRATOR_TENANT_SETTINGS)
    login_page.login()
    return AdministratorTenantSettingPage(py=py, context={})
