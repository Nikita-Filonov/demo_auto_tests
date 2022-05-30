import allure
import pytest

from settings import RERUNS, RERUNS_DELAY, DEFAULT_USER
from utils.allure.stories.ui.administrator import AdministratorStory


@pytest.mark.ui
@pytest.mark.administrator_groups
@allure.epic('Core LMS')
@allure.feature('Administrator (UI)')
@allure.story(AdministratorStory.GROUPS.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestAdministratorGroupsUi:

    @allure.id("4306")
    @allure.title('Administrator group "Create" and "Cancel" button (UI)')
    def test_administrator_user_create_and_cancel_button(self, group_page):
        group_page.create_group_button.click()
        group_page.create_group_title.is_visible()
        group_page.cancel_form_button.click()
        group_page.groups_title.is_visible()

    @allure.id("4298")
    @allure.title('Administrator create group (UI)')
    def test_administrator_create_group(self, new_group_page):
        new_group_page.group_form.fill()
        new_group_page.click_create()
        new_group_page.visit_entity()
        new_group_page.group_form.validate()
        new_group_page.owners_tab.click()
        new_group_page.user_present_in_gird(DEFAULT_USER)

    @allure.id("4305")
    @allure.title('Administrator change group (UI)')
    def test_administrator_change_group(self, edit_group_page):
        edit_group_page.group_form.fill()
        edit_group_page.click_update()
        edit_group_page.visit_entity()
        edit_group_page.group_form.validate()
