from typing import Optional

from utils.ui.components.component import Component


class Alert(Component):
    """
    Base button component

    Example:
        >>> alert = Alert('some_locator', 'My Alert')
    """

    def __init__(self, locator, text):
        super().__init__(locator)
        self._locator = locator
        self._text = text

    @property
    def type_of(self):
        return 'alert'

    @property
    def name(self) -> Optional[str]:
        return self._text
