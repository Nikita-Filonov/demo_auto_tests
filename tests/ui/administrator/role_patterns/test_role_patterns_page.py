import allure
import pytest

from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.ui.administrator import AdministratorStory


@pytest.mark.ui
@pytest.mark.administrator_role_patterns
@allure.epic('Core LMS')
@allure.feature('Administrator (UI)')
@allure.story(AdministratorStory.ROLE_PATTERNS.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestAdministratorRolePatternsUi:
    @allure.id("4340")
    @allure.title('Admin clicks "Create" and "Cancel" button for new role pattern (UI)')
    def test_admin_click_create_and_cancel_button_for_new_role_pattern(self, role_patterns_page):
        role_patterns_page.create_new_role_pattern_button.click()
        role_patterns_page.create_role_patterns_title.is_visible()
        role_patterns_page.cancel_form_button.click()
        role_patterns_page.role_patterns_title.is_visible()

    @allure.id("4341")
    @allure.title('Admin create role pattern (UI)')
    def test_admin_create_role_pattern(self, new_role_pattern_page):
        new_role_pattern_page.create_role_pattern_form.fill()
        new_role_pattern_page.click_create()
        new_role_pattern_page.visit_entity()
        new_role_pattern_page.create_role_pattern_form.validate()

    @allure.id("4342")
    @allure.title('Admin change role pattern (UI)')
    def test_admin_change_role_pattern(self, edit_role_pattern_page):
        edit_role_pattern_page.update_role_pattern_form.fill()
        edit_role_pattern_page.scope_type_input.is_disabled()
        edit_role_pattern_page.click_update()
        edit_role_pattern_page.visit_entity()
        edit_role_pattern_page.update_role_pattern_form.validate()
        edit_role_pattern_page.scope_type_input.have_value(edit_role_pattern_page.context['scopeType'])
