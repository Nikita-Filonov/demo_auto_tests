from typing import Union

from multipledispatch import dispatch

from utils.api.validation.messages.property_validation_message import PropertyValidationMessage


class RangeValidationMessage(PropertyValidationMessage):
    VALUE_TYPING = Union[float, int]
    message_format_greater_than = "{0}={1} out of range. Minimum value: {2}"
    message_format_in_range = "{0}={1} out of range. Minimum value: {2}, Maximum value: {3}"

    @dispatch(str, (float, int), (float, int))
    def __init__(self, property_name: str, actual_value: VALUE_TYPING, min_value: VALUE_TYPING):
        super().__init__(property_name=property_name)

        self.format = self.message_format_greater_than
        self.parameters = {
            'Property': property_name,
            'ActualValue': actual_value,
            'MinValue': min_value
        }

    @dispatch(str, (float, int), (float, int), (float, int))
    def __init__(
            self,
            property_name: str,
            actual_value: VALUE_TYPING,
            min_value: VALUE_TYPING,
            max_value: VALUE_TYPING
    ):
        self.format = self.message_format_in_range
        self.parameters = {
            'Property': property_name,
            'ActualValue': actual_value,
            'MinValue': min_value,
            'MaxValue': max_value
        }

    @property
    def type(self):
        return 'Range'
