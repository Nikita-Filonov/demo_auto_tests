from typing import Optional

from utils.ui.components.component import Component


class Text(Component):
    def __init__(self, locator, name=None):
        super().__init__(locator)
        self._locator = locator
        self._name = name

    @property
    def type_of(self):
        return 'text'

    @property
    def name(self) -> Optional[str]:
        return self._name

    def get_text(self, **kwargs):
        """
        Get text of the current Element
        Example:
            self.element(some_id='some_id').text()
        """
        return self.element(**kwargs).text()
