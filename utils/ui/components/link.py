from typing import Optional

from utils.ui.components.button import Button


class Link(Button):
    """
    Base link component

    Example:
        >>> link = Link('some_locator', 'My Link')
    """

    def __init__(self, locator, text):
        super().__init__(locator, text)
        self._text = text

    @property
    def type_of(self):
        return 'link'

    @property
    def name(self) -> Optional[str]:
        return self._text
