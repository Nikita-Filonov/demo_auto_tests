import pytest

from base.ui.administrator.users.users_page import AdministratorUsersPage
from base.ui.login_page import LoginPage, UsersViews


@pytest.fixture(scope='function')
def users_page(py) -> AdministratorUsersPage:
    login_page = LoginPage(py=py, view=UsersViews.ADMINISTRATOR_USERS)
    login_page.login()

    return AdministratorUsersPage(py=py, context={})


@pytest.fixture(scope='function')
def new_user_page(py) -> AdministratorUsersPage:
    login_page = LoginPage(py=py, view=UsersViews.ADMINISTRATOR_USERS_FORM, user_id='new')
    login_page.login()

    return AdministratorUsersPage(py=py, context={})


@pytest.fixture(scope='function')
def edit_user_page(py, user_role) -> AdministratorUsersPage:
    login_page = LoginPage(py=py, view=UsersViews.ADMINISTRATOR_USERS_FORM, user_id=user_role['userId'])
    login_page.login()

    return AdministratorUsersPage(py=py, context=user_role)
