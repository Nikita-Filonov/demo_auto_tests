from typing import Union, List, Optional

import allure

from utils.ui.components.checkbox import Checkbox
from utils.ui.components.input import Input
from utils.ui.components.textarea import Textarea


class Form:
    """
    Base input component

    Example:
        >>> some_form = Form([Input('some-locator'), Textarea('some-locator')], [Checkbox('some-checkbox')])
    """

    def __init__(self, fields: List[Union[Input, Textarea]], selects: Optional[List[Checkbox]] = None):
        self._fields = fields
        self._selects = selects or []

    @property
    def name(self, selects=None):
        return selects.name

    def reset_fields(self):
        for field in self._fields:
            field.cached_value = None

    def reset_selects(self):
        for select in self._selects:
            select.checked = select.default_checked

    def fill(self, **kwargs):
        """
        Abstract method form method which can be used to
        fill the form based on ``fields``

        Pass kwargs for dynamic locators
        """
        self.reset_fields()

        for field in self._fields:
            should_be_cleared = bool(field.get_attribute('value'))
            if should_be_cleared:
                field.clear(**kwargs)

            field.type(**kwargs)

        self.set_description()

    def validate(self, **kwargs):
        """
        Abstract method which can be used to check
        values in the form

        Pass kwargs for dynamic locators
        """
        for field in self._fields:
            field.have_value(field.cached_value, **kwargs)

        self.reset_fields()

    def select(self, force=True, **kwargs):
        """
        Abstract method form method which can be used to
        select checkboxes in the form based on ``selects``

        Pass kwargs for dynamic locators
        """
        self.reset_selects()
        for select in self._selects:
            select.checked = True
            select.click(force=force, **kwargs)

        self.set_description()

    def validate_select(self, **kwargs):
        """
        Abstract method which can be used to check
        selected checkboxes in the form

        Pass kwargs for dynamic locators
        """
        for select in self._selects:
            if select.checked:
                select.is_checked(**kwargs)

            else:
                select.is_unchecked(**kwargs)

        self.reset_selects()

    @property
    def payload(self) -> dict:
        return {field.name: field.cached_value for field in self._fields}

    def set_description(self):
        description = ''.join([f'Field: {field}, Value: {value}\n' for field, value in self.payload.items()])
        allure.dynamic.description(description)
