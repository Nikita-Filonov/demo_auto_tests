import pytest

from base.ui.administrator.objectives.objectives_page import ObjectiveAdministrationPage
from base.ui.login_page import LoginPage, UsersViews


@pytest.fixture(scope='function')
def objectives_page(py) -> ObjectiveAdministrationPage:
    login_page = LoginPage(py=py, view=UsersViews.OBJECTIVES_PAGE)
    login_page.login()

    return ObjectiveAdministrationPage(py=py, context={})


@pytest.fixture(scope='function')
def objective_page(py, objective_function) -> ObjectiveAdministrationPage:
    login_page = LoginPage(py=py, view=UsersViews.OBJECTIVE_PAGE, objective_id=objective_function['id'])
    login_page.login()

    return ObjectiveAdministrationPage(py=py, context={'objective': objective_function})


@pytest.fixture(scope='function')
def new_objective_page(py) -> ObjectiveAdministrationPage:
    login_page = LoginPage(py=py, view=UsersViews.OBJECTIVE_PAGE_LTI_FORM)
    login_page.login()

    return ObjectiveAdministrationPage(py=py, context={})
