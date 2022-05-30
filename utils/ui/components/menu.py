from typing import Optional

from utils.ui.components.button import Button


class Menu(Button):
    """
    Base menu component

    Example:
        >>> menu = Menu('some_locator', 'My Menu')
    """

    def __init__(self, locator, text):
        super().__init__(locator, text)
        self._text = text

    @property
    def type_of(self):
        return 'menu'

    @property
    def name(self) -> Optional[str]:
        return self._text

    @property
    def text(self):
        return self._text
