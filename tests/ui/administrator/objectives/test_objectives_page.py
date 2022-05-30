import allure
import pytest

from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.ui.administrator import AdministratorStory


@pytest.mark.ui
@pytest.mark.administrator_objectives
@allure.epic('Core LMS')
@allure.feature('Administrator (UI)')
@allure.story(AdministratorStory.OBJECTIVES.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestObjectivesAdministrationUi:
    @allure.id("4317")
    @allure.title('Admin clicks "Create" and "Cancel" button for new text objective (UI)')
    def test_admin_click_create_and_cancel_button_for_new_text_objective(self, objectives_page):
        objectives_page.create_new_objective_button.click()
        objectives_page.create_new_text_button.click()
        objectives_page.create_objective_title.is_visible()
        objectives_page.cancel_form_button.click()
        objectives_page.objectives_title.is_visible()

    @allure.id("4321")
    @allure.title('Admin clicks "Open tool" button on objective page (UI)')
    def test_admin_click_open_tool_button_on_objective_page(self, objective_page):
        objective_page.open_tool_button.click()
        objective_page.check_open_tool()
