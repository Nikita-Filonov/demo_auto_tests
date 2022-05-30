import pytest

from base.ui.administrator.for_grading.for_grading_page import ForGradingPage
from base.ui.instructor.review_course import ReviewCoursePage
from base.ui.login_page import LoginPage, UsersViews
from models.users.role import SupportedRoles


@pytest.fixture(scope='function')
def in_grade_review_course_page(py, in_grade_workflow_ui) -> ReviewCoursePage:
    """Author course details page constructor"""
    workflow_id = in_grade_workflow_ui[SupportedRoles.LEARNER]['workflow_id']
    login_page = LoginPage(py=py, view=UsersViews.INSTRUCTOR_FOR_GRADING_REVIEW, workflow_id=workflow_id)
    login_page.login()

    return ReviewCoursePage(py=py, context=in_grade_workflow_ui)


@pytest.fixture(scope='function')
def graded_review_course_page(py, graded_workflow_ui) -> ReviewCoursePage:
    """Author course details page constructor"""
    workflow_id = graded_workflow_ui[SupportedRoles.LEARNER]['workflow_id']
    login_page = LoginPage(py=py, view=UsersViews.INSTRUCTOR_FOR_GRADING_REVIEW, workflow_id=workflow_id)
    login_page.login()

    return ReviewCoursePage(py=py, context=graded_workflow_ui)


@pytest.fixture(scope='function')
def for_grading_page(request, py) -> ForGradingPage:
    options = getattr(request, 'param', {})
    login_page = LoginPage(py=py, view=UsersViews.ADMINISTRATOR_FOR_GRADING, **options)
    login_page.login(should_login=options.get('should_login', True))
    return ForGradingPage(py=py)
