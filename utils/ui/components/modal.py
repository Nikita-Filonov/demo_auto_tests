from typing import Optional

import allure

from utils.ui.components.button import Button
from utils.utils import wait


class Modal(Button):
    """
    Base menu component

    Example:
        >>> modal = Modal('some_locator', 'My Modal')
    """

    def __init__(self, locator, name):
        super().__init__(locator, name)
        self._name = name

    @property
    def type_of(self):
        return 'modal window'

    @property
    def name(self) -> Optional[str]:
        return self._name

    def click(self, **kwargs):
        with allure.step(f'User focusing on {self.type_of} "{self.name}"'):
            wait(
                lambda: self.element(**kwargs).click() is self.py,
                waiting_for=f'Until {self.type_of} "{self.name}" focused'
            )
