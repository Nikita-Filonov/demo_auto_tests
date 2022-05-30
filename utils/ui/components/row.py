from typing import Optional

import allure

from settings import WAIT_TIMEOUT
from utils.ui.components.component import Component


class Row(Component):
    """
    Base row component

    Example:
        >>> row = Row('some_locator', 'My Row')
    """

    def __init__(self, locator, column):
        super().__init__(locator)
        self._locator = locator
        self._column = column

    @property
    def type_of(self):
        return 'table row'

    @property
    def name(self) -> Optional[str]:
        return self._column

    def is_visible(self, text: Optional[str] = None, **kwargs):
        safe_text = str(text)
        step = f'Checking that {self.type_of} of column "{self._column}" with text "{safe_text}" present on the page'
        with allure.step(step):
            self.element(**kwargs).should(timeout=WAIT_TIMEOUT).be_visible()
            if text is not None:
                self.element(**kwargs).should(timeout=WAIT_TIMEOUT).have_text(safe_text)
