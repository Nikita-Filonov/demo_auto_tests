from abc import ABC, abstractmethod
from typing import Optional

import allure
from pylenium.driver import Pylenium
from pylenium.element import Element, Elements
from selenium.common.exceptions import TimeoutException

from settings import WAIT_TIMEOUT
from utils.utils import wait


class Py:
    """Wrapper for to keep pylenium instance"""
    py: Pylenium = None

    @classmethod
    def set_py(cls, py: Pylenium):
        cls.py = py


class Component(ABC):
    """Abstract component class"""

    LOCATOR_KEY = 'locator'

    def __init__(self, locator):
        self._locator = locator

    @property
    @abstractmethod
    def type_of(self) -> str:
        """Abstract method for define component type"""
        return 'component'

    @property
    def name(self) -> Optional[str]:
        return

    @property
    def locator(self):
        return self._locator

    @property
    def py(self):
        """
        Pylenium instance which should be used for
        interactions with element on the page
        """
        return Py.py

    def element(self, timeout: int = None, **kwargs) -> Element:
        """
        Base element which should be used to work with component.

        Example:
            self.element().click()
            self.element(some_id='some_id').click() # with dynamic component
        """
        locator = kwargs.pop(self.LOCATOR_KEY, self._locator)
        safe_locator = locator(self._locator, **kwargs) if callable(locator) else locator.format(**kwargs)

        return self.py.getx(safe_locator, timeout=timeout or WAIT_TIMEOUT)

    def element_into_view(self, **kwargs) -> Element:
        """
        Same as ``element`` but will scroll to the element until the element in view
        """
        return self.element(**kwargs).scroll_into_view()

    def elements(self, **kwargs) -> Elements:
        """
        Base method which will return list of elements.

        Example:
            self.elements() -> [...]
            self.elements(some_id='some_id') -> [...] # with dynamic component
        """
        return self.py.findx(self._locator.format(**kwargs), timeout=WAIT_TIMEOUT)

    def get_attribute(self, attribute, **kwargs):
        """
        Get attribute by xpath for element

        :arg
        attribute: some attribute from html/xml tag

        Example:
            self.element(some_id='some_id').get_attribute(attribute="data-tooltip") # with dynamic component
        """
        return self.element(**kwargs).get_attribute(attribute)

    def is_visible(self, **kwargs):
        """Used to check if element is displayed on the page"""
        with allure.step(f'{self.type_of.title()} "{self.name}" should be visible'):
            wait(
                lambda: self.element_into_view(**kwargs).should(timeout=WAIT_TIMEOUT).be_visible(),
                waiting_for=f'Until "{self.name}" {self.type_of} to be visible'
            )

    def not_visible(self, **kwargs):
        """Used to check tht element does not exists in the DOM"""
        with allure.step(f'{self.type_of.title()} "{self.name}" should not be visible'):
            try:
                self.element(timeout=1, **kwargs)
                visible = True
            except TimeoutException:
                visible = False

            if visible:
                raise AssertionError(f'Expected that {self.type_of} "{self.name}" should not be visible')

    def is_disabled(self, **kwargs):
        """Used to check if element is disabled"""
        with allure.step(f'{self.type_of.title()} "{self.name}" should be disabled'):
            wait(
                lambda: self.element_into_view(**kwargs).should(timeout=WAIT_TIMEOUT).be_disabled(),
                waiting_for=f'Until "{self.name}" {self.type_of} to be disabled'
            )

    def disappear(self, **kwargs):
        """Used to check if element is disappeared"""
        with allure.step(f'{self.type_of.title()} "{self.name}" should be disappear'):
            wait(
                lambda: self.element(**kwargs).should(timeout=WAIT_TIMEOUT).disappear(),
                waiting_for=f'Until "{self.name}" {self.type_of} to be disappear'
            )

    def contains_text(self, text, **kwargs):
        with allure.step(f'{self.type_of.title()} "{self.name}" should contain the text "{text}"'):
            self.element(**kwargs).should(timeout=WAIT_TIMEOUT).contain_text(text)

    def not_have_text(self, text, **kwargs):
        with allure.step(f'{self.type_of.title()} "{self.name}" should not have text "{text}"'):
            self.element(**kwargs).should(timeout=WAIT_TIMEOUT).not_have_text(text)

    def hover(self, **kwargs):
        with allure.step(f'User hover over {self.type_of} "{self.name}"'):
            wait(
                lambda: self.element(**kwargs).hover() is self.py,
                waiting_for=f'Until {self.type_of} "{self.name}" hovered'
            )
