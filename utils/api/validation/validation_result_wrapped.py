from abc import ABC
from typing import List, Dict

from utils.api.validation.messages.validation_message import ValidationMessage


class ValidationResultWrapped(ABC):
    """
    Abstract validation result builder. Implements
    interface for the building validation result, based
    on validation messages objects

    Can not be used it self, have to be inherited

    Ref to: https://youtrack.alemira.dev/issue/ALMS-1327
    """

    def __init__(self):
        super().__init__()
        self._internal: Dict[str, List[ValidationMessage]] = {}
        self._is_valid = True

    @property
    def result(self):
        return self._internal

    def _add(self, key: str, message: ValidationMessage):
        """Add validation message to the validation result"""
        value = [*self._internal[key], message] if (key in self._internal.keys()) else [message]
        self._internal[key] = value

    def _add_range(self, key: str, messages: List[ValidationMessage]):
        """Add multiple validation messages to the validation result"""
        value = [*self._internal[key], *messages] if (key in self._internal.keys()) else messages
        self._internal[key] = value

    def serialize(self) -> Dict[str, List[dict]]:
        """
        Returns the complicated structure of the validation result

        Ref to: https://youtrack.alemira.dev/issue/ALMS-1327
        """
        return {key: list(map(lambda v: v.serialize(), values)) for key, values in self.result.items()}

    def simplify(self) -> Dict[str, List[str]]:
        """
        Returns the simplified result of the validation result

        Ref to: https://youtrack.alemira.dev/issue/ALMS-1327
        """
        return {key: list(map(lambda v: v.message, values)) for key, values in self.result.items()}
