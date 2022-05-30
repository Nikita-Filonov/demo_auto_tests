from enum import Enum

import allure
from pylenium.driver import Pylenium

from base.ui.base_page import BasePage
from settings import LEARNER_URL, DEFAULT_USER, ADMIN_URL, AUTHOR_URL


class UsersViews(Enum):
    """Represents routes for pages"""
    LEARNER = LEARNER_URL
    LEARNER_PROFILE_PAGE = LEARNER_URL + '/profile'
    LEARNER_COURSE_PAGE = LEARNER_URL + '/courses/{objective_id}/{objective_workflow_aggregate_id}'

    ADMINISTRATOR_USERS = ADMIN_URL + '/users'
    ADMINISTRATOR_USERS_FORM = ADMIN_URL + '/users/{user_id}'
    ADMINISTRATOR_GROUPS = ADMIN_URL + '/groups'
    ADMINISTRATOR_GROUPS_FORM = ADMIN_URL + '/groups/{group_id}'

    ADMINISTRATOR_FOR_GRADING = ADMIN_URL + '/reports/for-grading'

    ADMINISTRATOR_ROLE_PATTERNS = ADMIN_URL + '/role-patterns'
    ADMINISTRATOR_NEW_ROLE_PATTERN = ADMIN_URL + '/role-patterns/new'
    ADMINISTRATOR_ROLE_PATTERN = ADMIN_URL + '/role-patterns/{role_pattern_id}'

    ADMINISTRATOR_TENANTS = ADMIN_URL + '/tenants'
    ADMINISTRATOR_NEW_TENANT = ADMIN_URL + '/tenants/new'
    ADMINISTRATOR_TENANT = ADMIN_URL + '/tenants/{tenant_id}'

    ADMINISTRATOR_TENANT_SETTINGS = ADMIN_URL + '/tenant-settings'

    OBJECTIVES_PAGE = ADMIN_URL + '/objectives'
    OBJECTIVE_PAGE_LTI_FORM = ADMIN_URL + '/objectives/new/lti'
    OBJECTIVE_PAGE_TEXT_FORM = ADMIN_URL + '/objectives/new/text'
    OBJECTIVE_PAGE = ADMIN_URL + '/objectives/{objective_id}'

    AUTHOR_COURSE_DETAILS = AUTHOR_URL + '/author/{request_id}'
    AUTHOR_NEW_EXERCISE = AUTHOR_URL + '/author/{request_id}/new-exercise'
    AUTHOR_EDIT_EXERCISE = AUTHOR_URL + '/author/{request_id}/exercise/{exercise_id}'

    RESOURCE_LIBRARIES_PAGE = ADMIN_URL + '/resource-libraries'
    RESOURCE_LIBRARY_NEW_FORM = ADMIN_URL + '/resource-libraries/new'
    RESOURCE_LIBRARY_PAGE = ADMIN_URL + '/resource-libraries/{resource_library_id}'

    INSTRUCTOR_FOR_GRADING_REVIEW = ADMIN_URL + '/reports/for-grading/review/{workflow_id}'


class LoginPage(BasePage):
    email_input = "input[type='email']"
    password_input = "input[type='password']"
    sign_in_button = "button[type=submit]"
    remember_login = '#Input_RememberLogin'
    forgot_password = '#forgot-password'

    def __init__(self, py: Pylenium, view: UsersViews = UsersViews.LEARNER, should_visit=True, **kwargs):
        super().__init__(py)

        if should_visit:
            py.visit(view.value.format(**kwargs))
        self.py = py

    @allure.step('User fill "Email" field to value "{1}"')
    def fill_email(self, value):
        self.py.get(self.email_input).type(value)

    @allure.step('User fill "Password" field to value "{1}"')
    def fill_password(self, value):
        self.py.get(self.password_input).type(value)

    @allure.step('User click "Sign in" button')
    def click_sign_in(self):
        self.py.get(self.sign_in_button).click()

    @allure.step('User click "Remember my login" checkbox')
    def click_remember_login(self):
        self.py.get(self.remember_login).click()

    @allure.step('User click "Forgot your password?" link')
    def click_forgot_password(self):
        self.py.get(self.forgot_password).click()

    def login(self, user=None, should_login=True):
        """Abstract method to login"""
        if not should_login:
            return

        if self.is_authorized:
            return

        with allure.step('User logs in'):
            self.fill_email(user or DEFAULT_USER['username'])
            self.fill_password(user or DEFAULT_USER['password'])
            self.click_sign_in()
            self.is_authorized = True
