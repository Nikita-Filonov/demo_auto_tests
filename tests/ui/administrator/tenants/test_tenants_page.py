import allure
import pytest

from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.ui.administrator import AdministratorStory


@pytest.mark.ui
@pytest.mark.administrator_tenants
@allure.epic('Core LMS')
@allure.feature('Administrator (UI)')
@allure.story(AdministratorStory.TENANTS.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestAdministratorTenantsUi:
    @allure.id("4345")
    @allure.title('Admin clicks "Create" and "Cancel" button for new tenant (UI)')
    def test_admin_click_create_and_cancel_button_for_new_tenant(self, tenants_page):
        tenants_page.create_new_tenant_button.click()
        tenants_page.create_tenant_title.is_visible()
        tenants_page.cancel_form_button.click()
        tenants_page.tenants_title.is_visible()

    @allure.id("4347")
    @allure.title('Admin create tenant (UI)')
    def test_admin_create_tenant(self, new_tenant_page):
        new_tenant_page.create_tenant_form.fill()
        new_tenant_page.click_create()
        new_tenant_page.visit_entity()
        new_tenant_page.update_tenant_form.validate()

    @allure.id("4346")
    @allure.title('Admin change tenant (UI)')
    def test_admin_change_tenant(self, edit_tenant_page):
        edit_tenant_page.update_tenant_form.fill()
        edit_tenant_page.click_update()
        edit_tenant_page.visit_entity()
        edit_tenant_page.update_tenant_form.validate()
