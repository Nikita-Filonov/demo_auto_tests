import re
from typing import Union

from utils.api.validation.exceptions import ValidationMessageException
from utils.api.validation.messages.validation_message import ValidationMessage
from utils.utils import find


class ValidationMessageFormat(ValidationMessage):
    message_formats = []

    def __init__(self, **kwargs):
        super().__init__()

        self._attrs = kwargs

    @property
    def attrs(self):
        return self._attrs

    @property
    def format(self):
        return self._resolve_format()

    @property
    def message(self):
        return self._format_message()

    def _resolve_parameters(self):
        if len(self.attrs) == 1:
            return {
                key: value
                for key, value in self.attrs.items()
                for key, value in {'property': key, 'value': value}.items()
            }

        return {
            key: value
            for index, (key, value) in enumerate(self.attrs.items())
            for key, value in {f'property{index + 1}': key, f'value{index + 1}': value}.items()
        }

    def _resolve_format(self) -> Union[str, None]:
        parameters = self.parameters
        message_format = find(lambda mf: len(re.findall(r'{\d}', mf)) == len(parameters), self.message_formats)

        if message_format is None:
            raise ValidationMessageException(f'Unable to find message format for "{len(parameters)}" args')

        return message_format

    def _format_message(self):
        parameters = self.parameters
        return self.format.format(*parameters.values())
