from typing import Dict, Optional

from utils.utils import to_pascal_case


class ValidationMessage:
    """
    Base validation message

    Implements base interface for creating validation message
    """

    TYPE = 'Type'
    MESSAGE = 'Message'
    FORMAT = 'Format'
    PARAMETERS = 'Parameters'

    SERIALIZABLE = (
        (TYPE, TYPE.lower()),
        (MESSAGE, MESSAGE.lower()),
        (FORMAT, FORMAT.lower()),
        (PARAMETERS, PARAMETERS.lower())
    )

    def __init__(
            self,
            message: Optional[str] = None,
            message_format: Optional[str] = None,
            parameters: Optional[Dict[str, object]] = None
    ):
        self._message = message
        self._format = message_format
        self._parameters: Dict[str, object] = parameters

    @property
    def type(self):
        return 'ValidationMessage'

    @property
    def message(self):
        return self.format.format(*self.parameters.values())

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        self._format = value

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        if value.get('property'):
            value['property'] = to_pascal_case(value['property'])

        self._parameters = value

    def __str__(self):
        return f'<{self.__class__.__name__}: {self.message}>'

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.message}>'

    def serialize(self) -> dict:
        """
        Used to serialize validation message
        """
        return {key: getattr(self, value) for key, value in self.SERIALIZABLE}
