import datetime
from typing import Any

import allure
from pylenium.element import Element
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from settings import WAIT_TIMEOUT
from utils.ui.components.component import Component
from utils.ui.constants import INPUT_DATETIME_FORMAT
from utils.utils import wait, file_name_or_path_resolve


class Input(Component):
    """
    Base input component

    Example:
        >>> some_input = Input('some_locator', 'My Input')
    """

    def __init__(self, locator, label=None, value=None, max_length: int = None):
        super().__init__(locator)
        self._locator = locator
        self._label = label
        self._value = value
        self._max_length = max_length
        self._cached_value = None

    @property
    def type_of(self):
        return 'input'

    @property
    def name(self):
        return self._label

    @property
    def value(self):
        if self._cached_value is None:
            self._cached_value = self._value() if callable(self._value) else self._value

        return self._cached_value

    @property
    def cached_value(self):
        return self._cached_value

    @cached_value.setter
    def cached_value(self, value):
        self._cached_value = value

    @staticmethod
    def format_value(value: Any):
        """Used to format any value to string."""
        if value is None:
            return ''

        if isinstance(value, (int, float)):
            value = str(value)

        if isinstance(value, datetime.datetime):
            value = value.strftime(INPUT_DATETIME_FORMAT)

        return value

    def label(self, **kwargs):
        """
        Used to get input label

        If no label provided, then it will try to get
        text/placeholder of element

        If unable to get element then it will return locator
        """
        if self._label:
            return self._label

        try:
            label = self.element(**kwargs).text()
            if not label:
                label = self.element(**kwargs).get_attribute('placeholder')
            return label
        except (StaleElementReferenceException, TimeoutException):
            return self._locator

    def type(self, value=None, **kwargs):
        label = self.label(**kwargs)
        safe_value = self.format_value(value if self.value is None else self.value)
        with allure.step(f'User type to {self.type_of} "{label}" value "{safe_value}"'):
            self.element(**kwargs).type(safe_value)

    def have_value(self, value, **kwargs):
        label = self.label(**kwargs)
        safe_value = self.format_value(value)
        with allure.step(f'{self.type_of.title()} "{label}" should have value "{safe_value}"'):
            wait(
                lambda: type(self.element_into_view(**kwargs)
                             .should(timeout=WAIT_TIMEOUT).have_value(safe_value)) is Element,
                waiting_for=f'Until {self.type_of} "{label}" to have value {safe_value}'
            )

    def not_have_value(self, value):
        return

    def is_readonly(self, **kwargs):
        label = self.label(**kwargs)
        with allure.step(f'Checking that {self.type_of} "{label}" is readonly'):
            wait(
                lambda: self.element_into_view(**kwargs).get_attribute('readonly'),
                waiting_for=f'Until {self.type_of} "{label}" with locator "{self._locator}" to be readonly'
            )

    def clear(self, **kwargs):
        label = self.label(**kwargs)
        with allure.step(f'Clearing {self.type_of} "{label}"'):
            self.element(**kwargs).clear()

    def attach_file(self, file_path, **kwargs):
        label = self.label(**kwargs)
        safe_file_name = file_name_or_path_resolve(file_path)
        with allure.step(f'User attach file "{safe_file_name}" to {self.type_of} "{label}"'):
            self.element(**kwargs).type(file_path)
