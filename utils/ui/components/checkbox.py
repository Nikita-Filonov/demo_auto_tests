from typing import Optional

import allure

from utils.ui.components.button import Button
from utils.utils import wait


class Checkbox(Button):
    """
    Base checkbox component

    Example:
        >>> checkbox = Checkbox('some_locator', 'My Checkbox')
    """

    def __init__(self, locator, text, default_checked=False):
        super().__init__(locator, text)
        self._locator = locator
        self._text = text
        self._checked = default_checked
        self._default_checked = default_checked

    @property
    def type_of(self):
        return 'checkbox'

    @property
    def name(self) -> Optional[str]:
        return self._text

    @name.setter
    def name(self, text):
        self._text = text

    @property
    def checked(self):
        return self._checked

    @property
    def default_checked(self):
        return self._default_checked

    @checked.setter
    def checked(self, checked):
        self._checked = checked

    def get_checkbox_status(self, attribute='value', **kwargs) -> bool:
        return self.get_attribute(attribute, **kwargs)

    def is_checked(self, attribute='value', **kwargs):
        with allure.step(f'{self.type_of} "{self.name}" is checked'):
            wait(
                lambda: self.get_checkbox_status(attribute, **kwargs),
                waiting_for=f'Until {self.type_of} "{self.name}" to be checked'
            )

    def is_unchecked(self, attribute='value', **kwargs):
        with allure.step(f'{self.type_of} "{self.name}" is unchecked'):
            wait(
                lambda: not self.get_checkbox_status(attribute, **kwargs),
                waiting_for=f'Until {self.type_of} "{self.name}" to be unchecked'
            )
