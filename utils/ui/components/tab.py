from typing import Optional

from utils.ui.components.button import Button


class Tab(Button):
    """
    Base tab component

    Example:
        >>> tab = Tab('some_locator', 'My Tab')
    """

    def __init__(self, locator, text):
        super().__init__(locator, text)
        self._locator = locator
        self._text = text

    @property
    def type_of(self):
        return 'tab'

    @property
    def name(self) -> Optional[str]:
        return self._text
