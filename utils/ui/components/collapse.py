from typing import Optional

import allure

from utils.ui.components.button import Button


class Collapse(Button):
    """
    Base collapse component

    Example:
        >>> collapse = Collapse('some_locator', 'My Collapse')
    """

    def __init__(self, locator, text, is_expanded=False):
        super().__init__(locator, text)
        self._is_expanded = is_expanded
        self._text = text

    @property
    def type_of(self):
        return 'collapse'

    @property
    def name(self) -> Optional[str]:
        return self._text

    @property
    def is_expanded(self):
        return self._is_expanded

    @property
    def state(self):
        return 'collapse' if self._is_expanded else 'expand'

    def click(self, **kwargs):
        with allure.step(f'User {self.state} {self._text}'):
            super().click(**kwargs)
            self._is_expanded = not self._is_expanded
