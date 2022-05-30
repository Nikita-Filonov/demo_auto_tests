from typing import Optional

from utils.ui.components.component import Component


class Icon(Component):
    """
    Base icon component

    Example:
        >>> icon = Icon('some_locator', 'My Icon')
    """

    def __init__(self, locator, text):
        super().__init__(locator)
        self._locator = locator
        self._text = text

    @property
    def type_of(self):
        return 'icon'

    @property
    def name(self) -> Optional[str]:
        return self._text
