from typing import Optional

import allure

from utils.ui.components.component import Component
from utils.utils import wait


class Button(Component):
    """
    Base button component

    Example:
        >>> button = Button('some_locator', 'My Button')
    """

    def __init__(self, locator, text):
        super().__init__(locator)
        self._locator = locator
        self._text = text

    @property
    def type_of(self):
        return 'button'

    @property
    def name(self) -> Optional[str]:
        return self._text

    @name.setter
    def name(self, text):
        self._text = text

    def click(self, force=False, **kwargs):
        with allure.step(f'User clicking {self.type_of} "{self.name}"'):
            wait(
                lambda: self.element_into_view(**kwargs).click(force=force) is self.py,
                waiting_for=f'Until {self.type_of} "{self.name}" clicked'
            )

    def is_clickable(self, **kwargs):
        with allure.step(f'User can click on {self.type_of} "{self.name}"'):
            wait(
                lambda: self.element(**kwargs).should().be_clickable(),
                waiting_for=f'Until {self.type_of} "{self.name}" is clickable'
            )
