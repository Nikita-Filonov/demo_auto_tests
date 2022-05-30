import allure
import pytest

from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.ui.administrator import AdministratorStory


@pytest.mark.ui
@pytest.mark.administrator_users
@allure.epic('Core LMS')
@allure.feature('Administrator (UI)')
@allure.story(AdministratorStory.USERS.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestAdministratorUsersUi:

    @allure.id("4263")
    @allure.title('Administrator clicks "Create" and "Cancel" button (UI)')
    def test_administrator_create_user_cancel_button(self, users_page):
        users_page.create_user_button.click()
        users_page.create_user_title.is_visible()
        users_page.cancel_form_button.click()
        users_page.users_title.is_visible()

    @allure.id("4264")
    @allure.title('Administrator create user (UI)')
    def test_administrator_create_user(self, new_user_page):
        new_user_page.user_form.fill()
        new_user_page.click_create()
        new_user_page.visit_entity()
        new_user_page.user_form.validate()

    @allure.id("4266")
    @allure.title('Administrator change user (UI)')
    def test_administrator_change_user(self, edit_user_page):
        edit_user_page.user_form.fill()
        edit_user_page.click_update()
        edit_user_page.visit_entity()
        edit_user_page.user_form.validate()
