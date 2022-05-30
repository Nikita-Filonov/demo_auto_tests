import pytest

from base.ui.administrator.tenants.tenants_page import AdministratorTenantsPage
from base.ui.login_page import LoginPage, UsersViews


@pytest.fixture(scope='function')
def tenants_page(py) -> AdministratorTenantsPage:
    login_page = LoginPage(py=py, view=UsersViews.ADMINISTRATOR_TENANTS)
    login_page.login()
    return AdministratorTenantsPage(py=py, context={})


@pytest.fixture(scope='function')
def new_tenant_page(py) -> AdministratorTenantsPage:
    login_page = LoginPage(py=py, view=UsersViews.ADMINISTRATOR_NEW_TENANT)
    login_page.login()
    return AdministratorTenantsPage(py=py, context={})


@pytest.fixture(scope='function')
def edit_tenant_page(py, tenant_function) -> AdministratorTenantsPage:
    login_page = LoginPage(py=py, view=UsersViews.ADMINISTRATOR_TENANT, tenant_id=tenant_function['id'])
    login_page.login()

    return AdministratorTenantsPage(py=py, context=tenant_function)
