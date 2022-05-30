from typing import Union

from multipledispatch import dispatch

from utils.api.validation.messages.property_validation_message import PropertyValidationMessage


class EntityAlreadyExistsPropertyValidationMessage(PropertyValidationMessage):
    message_single_key_format = "{1} with {0} '{2}' already exists"

    @dispatch(str, str, (str, int, float))
    def __init__(self, entity_name: str, property_name: str, value: Union[str, int, float]):
        super().__init__(property_name=property_name)

        self.format = self.message_single_key_format
        self.parameters = {
            'property': property_name,
            'entity': entity_name,
            'value': value
        }

    @property
    def type(self):
        return 'EntityAlreadyExistsProperty'
