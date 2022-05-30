from typing import Optional

import allure

from utils.ui.components.button import Button


class Item(Button):
    """
    Base item component

    Example:
        >>> item = Item('some_locator', 'My Item')
    """

    def __init__(self, locator, text):
        super().__init__(locator, text)

    @property
    def type_of(self):
        return 'item'

    @property
    def name(self) -> Optional[str]:
        return self._text

    @name.setter
    def name(self, text):
        self._text = text

    def count(self, **kwargs) -> int:
        with allure.step(f'Getting length of the "{self.name}" {self.type_of}s displayed on the page'):
            return self.elements(**kwargs).length()
