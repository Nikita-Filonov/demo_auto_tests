from typing import Optional

from utils.ui.components.button import Button


class Select(Button):
    """
    Base button component

    Example:
        >>> select = Select('some_locator', 'My Select')
    """

    def __init__(self, locator, text):
        super().__init__(locator, text)
        self._locator = locator
        self._text = text

    @property
    def type_of(self):
        return 'select'

    @property
    def name(self) -> Optional[str]:
        return self._text
