from typing import List

from multipledispatch import dispatch

from utils.api.validation.messages.property_validation_message import PropertyValidationMessage
from utils.api.validation.messages.validation_message import ValidationMessage
from utils.api.validation.validation_result_wrapped import ValidationResultWrapped


class ValidationResult(ValidationResultWrapped):
    """
    Base validation result builder. Can accept validation
    messages objects and manage them into validation result
    """

    COMMON_MESSAGES_KEY = '_'

    def __init__(self):
        super().__init__()

    @property
    def is_valid(self):
        """Returns is result valid, based on number of validation messages"""
        return len(self._internal) == 0

    @dispatch(PropertyValidationMessage)
    def add_message(self, message: PropertyValidationMessage):
        """Adding property validation message to the validation result"""
        self._add(message.property_name, message)
        return self

    @dispatch(ValidationMessage)
    def add_message(self, message: ValidationMessage):
        """Adding common validation message to the validation result"""
        self._add(self.COMMON_MESSAGES_KEY, message)
        return self

    def add_common_messages(self, messages: List[ValidationMessage]):
        """Adding list of common validation messages to the validation result"""
        self._add_range(self.COMMON_MESSAGES_KEY, messages)
