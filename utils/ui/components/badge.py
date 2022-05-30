from typing import Optional

from utils.ui.components.component import Component


class Badge(Component):
    """
    Base button component

    Example:
        >>> button = Badge('some_locator', 'My Badge')
    """

    def __init__(self, locator, text):
        super().__init__(locator)
        self._locator = locator
        self._text = text

    @property
    def type_of(self):
        return 'badge'

    @property
    def name(self) -> Optional[str]:
        return self._text
