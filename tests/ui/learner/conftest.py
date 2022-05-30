import pytest
from alms_integration import get_objective_workflow_aggregate

from base.api.users.objectives.objectives import get_objective
from base.ui.learner.courses.course import CoursePage
from base.ui.learner.courses.courses import CoursesPage
from base.ui.learner.courses.profile import ProfilePage
from base.ui.login_page import UsersViews, LoginPage
from models.users.objective_access import ObjectiveAccesses
from models.users.role import SupportedRoles
from parameters.courses.ui.context import context_template


@pytest.fixture(scope='function')
def courses_page(request, py, objective_access) -> CoursesPage:
    """Courses page constructor"""
    options = getattr(request, 'param', {})
    login_page = LoginPage(py=py, view=UsersViews.LEARNER, **options)
    login_page.login(should_login=options.get('should_login', True))

    objective = get_objective(objective_access['objectiveId']).json()
    return CoursesPage(py=py, context={**context_template, 'objective': objective})


@pytest.fixture(scope='function')
def profile_page(request, py) -> ProfilePage:
    """Profile page content"""
    options = getattr(request, 'param', {})
    login_page = LoginPage(py=py, view=UsersViews.LEARNER_PROFILE_PAGE, **options)
    login_page.login(should_login=options.get('should_login', True))

    return ProfilePage(py=py, context=context_template)


@pytest.fixture(scope='function')
def profile_page_with_course(py, approved_workflow_ui) -> ProfilePage:
    """Profile page content with course results"""
    objective_id = approved_workflow_ui[SupportedRoles.OBSERVER]['objective_id']
    login_page = LoginPage(py=py,
                           view=UsersViews.LEARNER_PROFILE_PAGE,
                           objective_id=objective_id
                           )
    login_page.login()
    return ProfilePage(py=py, context=approved_workflow_ui)


@pytest.fixture(scope='function')
def course_page(py, started_course_ui) -> CoursePage:
    """Learner course page"""
    objective_id = started_course_ui[SupportedRoles.LEARNER]['objective_id']
    objective_workflow_aggregate_id = started_course_ui[SupportedRoles.LEARNER]['objective_workflow_aggregate_id']
    login_page = LoginPage(py=py,
                           view=UsersViews.LEARNER_COURSE_PAGE,
                           objective_id=objective_id,
                           objective_workflow_aggregate_id=objective_workflow_aggregate_id)
    login_page.login()

    return CoursePage(py=py, context=started_course_ui)


@pytest.fixture(scope='function')
def course_details_page(py, objective_access) -> CoursePage:
    """Learner course details page"""
    objective_id = objective_access[ObjectiveAccesses.objective_id.json]
    objective_workflow_aggregate = get_objective_workflow_aggregate(objective_id).json()

    login_page = LoginPage(py=py,
                           view=UsersViews.LEARNER_COURSE_PAGE,
                           objective_id=objective_id,
                           objective_workflow_aggregate_id=objective_workflow_aggregate['id'])

    login_page.login()

    return CoursePage(py=py, context=context_template)


@pytest.fixture(scope='function')
def finished_course_page(py, approved_workflow_ui) -> CoursePage:
    """Learner finished course page"""
    objective_id = approved_workflow_ui[SupportedRoles.LEARNER]['objective_id']
    objective_workflow_aggregate_id = approved_workflow_ui[SupportedRoles.LEARNER]['objective_workflow_aggregate_id']

    login_page = LoginPage(py=py,
                           view=UsersViews.LEARNER_COURSE_PAGE,
                           objective_id=objective_id,
                           objective_workflow_aggregate_id=objective_workflow_aggregate_id)
    login_page.login()

    return CoursePage(py=py, context=approved_workflow_ui)
