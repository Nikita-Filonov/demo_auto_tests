import pytest

from base.ui.administrator.role_patterns.role_patterns_page import AdministratorRolePatternsPage
from base.ui.login_page import LoginPage, UsersViews


@pytest.fixture(scope='function')
def role_patterns_page(py) -> AdministratorRolePatternsPage:
    login_page = LoginPage(py=py, view=UsersViews.ADMINISTRATOR_ROLE_PATTERNS)
    login_page.login()
    return AdministratorRolePatternsPage(py=py, context={})


@pytest.fixture(scope='function')
def new_role_pattern_page(py) -> AdministratorRolePatternsPage:
    login_page = LoginPage(py=py, view=UsersViews.ADMINISTRATOR_NEW_ROLE_PATTERN)
    login_page.login()
    return AdministratorRolePatternsPage(py=py, context={})


@pytest.fixture(scope='function')
def edit_role_pattern_page(py, role_pattern) -> AdministratorRolePatternsPage:
    login_page = LoginPage(py=py, view=UsersViews.ADMINISTRATOR_ROLE_PATTERN, role_pattern_id=role_pattern['id'])
    login_page.login()

    return AdministratorRolePatternsPage(py=py, context=role_pattern)
