import allure
import pytest

from base.ui.administrator.resource_library.resource_library_page import get_resource_library_checkbox_locator, \
    to_change_resource_library_payload
from parameters.courses.ui.users.lti_form import lti_form_parameters
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.ui.administrator import AdministratorStory


@pytest.mark.ui
@pytest.mark.administrator_resource_library
@allure.epic('Core LMS')
@allure.feature('Administrator (UI)')
@allure.story(AdministratorStory.RESOURCE_LIBRARY.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestAdministratorResourceLibraryUi:

    @allure.id("4671")
    @allure.title('Admin clicks "Create" and "Cancel" button for new resource library (UI)')
    def test_admin_click_create_and_cancel_button_for_new_resource_library(self, resource_libraries_page):
        resource_libraries_page.add_new_resource_library_button.click()
        resource_libraries_page.add_new_resource_library_title.is_visible()
        resource_libraries_page.cancel_form_button.click()
        resource_libraries_page.resource_library_title.is_visible()

    @allure.id("4669")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1325',
        name='Fix Create button in UI resource library (Public and Private file type)'
    )
    @pytest.mark.parametrize('lti_form', lti_form_parameters)
    @allure.title('Admin create resource library (UI)')
    def test_admin_create_resource_library(self, new_resource_library_page, lti_form):
        new_resource_library_page.set_value_from_lti_menu(lti_form['model'])
        lti_form['form'].fill()
        lti_form['form'].select()
        new_resource_library_page.click_create()
        new_resource_library_page.visit_entity()
        lti_form['form'].validate()
        lti_form['form'].validate_select(locator=get_resource_library_checkbox_locator)
        new_resource_library_page.check_value_in_lti_menu(lti_form['type'])

    @allure.id("4670")
    @pytest.mark.parametrize(
        'resource_library, lti_form',
        to_change_resource_library_payload(lti_form_parameters),
        indirect=['resource_library']
    )
    @allure.title('Admin change resource library (UI)')
    def test_admin_change_resource_library(self, resource_library, lti_form, edit_resource_library_page):
        lti_form['form'].fill()
        lti_form['form'].select()
        edit_resource_library_page.click_update()
        edit_resource_library_page.visit_entity()
        lti_form['form'].validate()
        lti_form['form'].validate_select(locator=get_resource_library_checkbox_locator)
        edit_resource_library_page.check_value_in_lti_menu(lti_form['type'])
