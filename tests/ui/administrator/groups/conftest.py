import pytest

from base.ui.administrator.groups.groups_page import AdministratorGroupsPage
from base.ui.login_page import LoginPage, UsersViews


@pytest.fixture(scope='function')
def group_page(py) -> AdministratorGroupsPage:
    login_page = LoginPage(py=py, view=UsersViews.ADMINISTRATOR_GROUPS)
    login_page.login()

    return AdministratorGroupsPage(py=py, context={})


@pytest.fixture(scope='function')
def new_group_page(py) -> AdministratorGroupsPage:
    login_page = LoginPage(py=py, view=UsersViews.ADMINISTRATOR_GROUPS_FORM, group_id='new')
    login_page.login()

    return AdministratorGroupsPage(py=py, context={})


@pytest.fixture(scope='function')
def edit_group_page(py, group_function) -> AdministratorGroupsPage:
    login_page = LoginPage(py=py, view=UsersViews.ADMINISTRATOR_GROUPS_FORM, group_id=group_function['id'])
    login_page.login()

    return AdministratorGroupsPage(py=py, context=group_function)
