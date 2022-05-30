from typing import Optional

from utils.ui.components.input import Input


class Textarea(Input):
    """
    Base textarea component

    Example:
        >>> textarea = Textarea('some_locator', 'My Textarea')
    """

    def __init__(self, locator, label=None, value=None):
        super().__init__(locator, label, value)
        self._locator = locator
        self._label = label
        self._value = value

    @property
    def type_of(self):
        return 'textarea'

    @property
    def name(self) -> Optional[str]:
        return self._label
