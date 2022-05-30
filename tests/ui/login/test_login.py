import allure
import pytest

from base.ui.login_page import LoginPage
from settings import RERUNS, RERUNS_DELAY, DEFAULT_USER
from utils.utils import random_string


@pytest.mark.ui
@pytest.mark.login
@allure.epic('Core LMS')
@allure.feature('Login (UI)')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestLoginUi:
    @allure.id("1290")
    @pytest.mark.parametrize(
        'courses_page',
        [{'should_visit': False, 'should_login': False}],
        indirect=['courses_page']
    )
    @allure.title('Login with valid credentials')
    def test_login_with_valid_credentials(self, login_page, courses_page):
        login_page.fill_email(DEFAULT_USER['username'])
        login_page.fill_password(DEFAULT_USER['password'])
        login_page.click_sign_in()
        courses_page.is_courses_page_location()

    @allure.id("1289")
    @allure.title('Login with invalid password')
    def test_login_with_invalid_password(self, login_page: LoginPage):
        login_page.fill_email(DEFAULT_USER['username'])
        login_page.fill_password(random_string())
        login_page.click_sign_in()

        assert login_page.py.contains('Invalid username or password')

    @allure.id("1330")
    @allure.title('Login with invalid email')
    def test_login_with_invalid_email(self, login_page: LoginPage):
        login_page.fill_email(random_string() + '@gmail.com')
        login_page.fill_password(DEFAULT_USER['password'])
        login_page.click_sign_in()

        assert login_page.py.contains('Invalid username or password')

    @allure.id("1332")
    @allure.title('Forgot password present on page')
    def test_forgot_password_present_on_page(self, login_page: LoginPage):
        assert login_page.py.contains('Forgot your password?')

    @allure.id("1331")
    @allure.title('Remember my login present on page')
    def test_remember_my_login_present_on_page(self, login_page: LoginPage):
        assert login_page.py.contains('Remember my login')

    @allure.id("1333")
    @pytest.mark.skip(reason='It is not working yet')
    @pytest.mark.parametrize(
        'courses_page',
        [{'should_visit': False, 'should_login': False}],
        indirect=['courses_page']
    )
    @allure.title('Login with "Remember my login"')
    def test_login_with_remember_my_login(self, login_page, courses_page):
        login_page.fill_email(DEFAULT_USER['username'])
        login_page.fill_password(DEFAULT_USER['password'])
        login_page.click_remember_login()
        login_page.click_sign_in()
        courses_page.is_courses_page_location()

    @allure.id("1334")
    @allure.title('Forgot password is clickable')
    def test_forgot_password_is_clickable(self, login_page: LoginPage):
        login_page.click_forgot_password()
        assert login_page.py.contains('Password recovery')
