from multipledispatch import dispatch

from utils.api.validation.messages.property_validation_message import PropertyValidationMessage
from utils.utils import to_pascal_case


class ReferencedEntityDoesNotExistPropertyValidationMessage(PropertyValidationMessage):
    message_single_key_format = "{1} referenced to {2} with {3} = '{4}' which does not exist or your permissions " \
                                "are not enough to access it"

    @dispatch(str, str, str, str, str)
    def __init__(
            self,
            property_name: str,
            entity_name: str,
            referenced_entity_name: str,
            referenced_entity_key: str,
            referenced_value: str
    ):
        super().__init__(property_name)

        self.format = self.message_single_key_format
        self.parameters = {
            "property": property_name,
            "entity": entity_name,
            "referencedEntity": referenced_entity_name,
            "referencedEntityKey": to_pascal_case(referenced_entity_key),
            "referencedValue": referenced_value
        }

    @property
    def type(self):
        return "ReferencedEntityDoesNotExistProperty"
