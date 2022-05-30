from multipledispatch import dispatch

from utils.api.validation.messages.validation_message import ValidationMessage


class ReferencedEntityDoesNotExistValidationMessage(ValidationMessage):
    message_single_key_format = "{0} referenced to {1} with {2} = '{3}' which does not exist or your permissions are " \
                                "not enough to access it"

    @dispatch(str, str, str, str)
    def __init__(self, entity_name: str, referenced_entity_name: str, referenced_entity_key: str, value: str):
        super().__init__()

        self.format = self.message_single_key_format
        self.parameters = {
            "entity": entity_name,
            "referencedEntity": referenced_entity_name,
            "referencedEntityKey": referenced_entity_key,
            "referencedValue": value
        }

    @property
    def type(self):
        return "ReferencedEntityDoesNotExist"
