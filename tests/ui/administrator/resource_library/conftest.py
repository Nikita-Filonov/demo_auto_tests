import pytest

from base.ui.administrator.resource_library.resource_library_page import AdministratorResourceLibraryPage
from base.ui.login_page import LoginPage, UsersViews


@pytest.fixture(scope='function')
def resource_libraries_page(py) -> AdministratorResourceLibraryPage:
    login_page = LoginPage(py=py, view=UsersViews.RESOURCE_LIBRARIES_PAGE)
    login_page.login()
    return AdministratorResourceLibraryPage(py=py, context={})


@pytest.fixture(scope='function')
def new_resource_library_page(py) -> AdministratorResourceLibraryPage:
    login_page = LoginPage(py=py, view=UsersViews.RESOURCE_LIBRARY_NEW_FORM)
    login_page.login()
    return AdministratorResourceLibraryPage(py=py, context={})


@pytest.fixture(scope='function')
def edit_resource_library_page(py, resource_library) -> AdministratorResourceLibraryPage:
    _, resource_library = resource_library
    login_page = LoginPage(py=py, view=UsersViews.RESOURCE_LIBRARY_PAGE, resource_library_id=resource_library['id'])
    login_page.login()

    return AdministratorResourceLibraryPage(py=py, context=resource_library)
