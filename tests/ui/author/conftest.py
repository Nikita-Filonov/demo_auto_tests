import pytest

from base.api.ztool.element import upload_file_to_element, get_element_files
from base.api.ztool.launch import get_launch
from base.ui.author.course_details import CourseDetailsPage
from base.ui.author.new_exercise import NewExercisePage
from base.ui.login_page import LoginPage, UsersViews
from models.users.role import SupportedRoles


@pytest.fixture(scope='function')
def author(request, course_ui):
    """Wrapper around ``course_ui`` that adding launch payload to the ``course_ui`` payload"""
    files = request.param['files'] if hasattr(request, 'param') else []
    element_id = course_ui['element']['element_id']

    author = get_launch(SupportedRoles.AUTHOR, element_id=element_id)
    request_id = author['request_id']

    for file in files:
        upload_file_to_element(request_id, element_id, file)

    element_files = get_element_files(request_id, element_id)

    return {**course_ui, 'files': element_files, SupportedRoles.AUTHOR: author}


@pytest.fixture(scope='function')
def course_details(py, author) -> CourseDetailsPage:
    """Author course details page constructor"""
    request_id = author[SupportedRoles.AUTHOR]['request_id']
    login_page = LoginPage(py=py, view=UsersViews.AUTHOR_COURSE_DETAILS, request_id=request_id)
    login_page.login()

    return CourseDetailsPage(py=py, context=author)


@pytest.fixture(scope='function')
def new_exercise(py, author) -> NewExercisePage:
    """Author new exercise page constructor"""
    request_id = author[SupportedRoles.AUTHOR]['request_id']
    login_page = LoginPage(py=py, view=UsersViews.AUTHOR_COURSE_DETAILS, request_id=request_id)
    login_page.login()

    return NewExercisePage(py=py, context=author)


@pytest.fixture(scope='function')
def course_files(course_details) -> CourseDetailsPage:
    course_details.files_tab.click()
    return course_details


@pytest.fixture(scope='function')
def course_dates(course_details) -> CourseDetailsPage:
    course_details.dates_tab.click()
    return course_details


@pytest.fixture(scope='function')
def author_submitted_workflow(course_dates, submitted_workflow_ui) -> CourseDetailsPage:
    """Opens author course details page with already submitted workflow"""
    course_dates.context = submitted_workflow_ui
    return course_dates


@pytest.fixture(scope='function')
def author_graded_workflow(course_dates, graded_workflow_ui) -> CourseDetailsPage:
    """Opens author course details page with already graded workflow"""
    course_dates.context = graded_workflow_ui
    return course_dates


@pytest.fixture(scope='function')
def author_approved_workflow(course_dates, approved_workflow_ui) -> CourseDetailsPage:
    """Opens author course details page with already grading approved workflow"""
    course_dates.context = approved_workflow_ui
    return course_dates
