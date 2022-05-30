from typing import Optional

import allure
import pytest
from pylenium.driver import Pylenium
from pylenium.element import Element

from base.api.users.tenant_settings.reset_tenant_settings import reset_tenant_settings
from settings import WAIT_TIMEOUT
from utils.assertions.files import assert_downloaded_file
from utils.ui.components.alert import Alert
from utils.ui.components.button import Button
from utils.ui.components.iframe import IFrame, without_iframe
from utils.ui.components.input import Input
from utils.ui.utils import wait_for


class BasePage:
    tool_iframe = IFrame('tooliframe')
    error_alert_message = Alert('//*[@data-qa="alert-message"]', 'Error alert')
    attach_file_input = Input('//input[@type="file"]', 'Attach file')
    confirm_modal_yes_button = Button('//*[@data-qa="confirm-modal-yes-button"]', 'Yes')
    confirm_modal_no_button = Button('//*[@data-qa="confirm-modal-no-button"]', 'No')
    is_authorized: bool = False

    wait_for = staticmethod(wait_for)
    assert_downloaded_file = staticmethod(assert_downloaded_file)

    def __init__(self, py: Pylenium):
        self.py = py

    def element_into_view(self, locator) -> Element:
        """
        Will scroll to the element until the element in view
        """
        return self.py.getx(locator, timeout=WAIT_TIMEOUT).scroll_into_view()

    @without_iframe(tool_iframe)
    def reload(self):
        with allure.step(f'User reloads the page {self.py.url()}'):
            self.py.reload()

    def text_present(self, text: str, native: bool = True):
        """
        Should be used to check if text present on the page

        native - if True then will use native text check from Pylenium.
        If False then will use custom check that need for some specific
        scenarios.
        """
        with allure.step(f'Checking that "{text}" present on the page'):
            if native:
                self.py.contains(text)
            else:
                locator = f'//*[text()[contains(.,"{text}")]]'
                self.element_into_view(locator).should().contain_text(text)

    def text_not_present(self, text: str):
        """Should be used to check if text not present on the page"""
        with allure.step(f'Checking that "{text}" not present on the page'):
            self.py.should(timeout=WAIT_TIMEOUT).not_contain(text)

    def element_present(self, locator: str, name: Optional[str] = None):
        """Should be used to check if element present on the page"""
        with allure.step(f'Checking that "{name}" present on the page'):
            self.element_into_view(locator).should(timeout=WAIT_TIMEOUT).be_visible()

    def element_should_have_text(self, locator: str, text: str, name: Optional[str] = None):
        with allure.step(f'Checking that "{name}" present having text "{text}"'):
            self.element_into_view(locator).should(timeout=WAIT_TIMEOUT).have_text(text)

    def error_alert_present(self):
        """Checking if error alert present on the page"""
        self.error_alert_message.is_visible()

    def error_alert_not_present(self):
        self.error_alert_message.not_visible()

    def click_confirm_modal_yes_button(self):
        self.confirm_modal_yes_button.click()

    def click_confirm_modal_no_button(self):
        self.confirm_modal_no_button.click()

    def upload_file(self, file_path: str):
        self.attach_file_input.attach_file(file_path=file_path)


class BaseUI:
    @pytest.fixture(autouse=True, scope='function')
    def reset_iframe(self):
        IFrame.on_iframe = False


class BaseTenantSettingsUI(BaseUI):
    @pytest.fixture(autouse=True, scope='function')
    def set_default_tenant_settings(self):
        reset_tenant_settings()
