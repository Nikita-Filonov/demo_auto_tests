from tests.ui.learner.conftest import *


@pytest.fixture(scope='function')
def login_page(py) -> LoginPage:
    """Login page constructor"""
    return LoginPage(py=py, view=UsersViews.LEARNER)
