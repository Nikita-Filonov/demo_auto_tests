from utils.api.validation.messages.validation_message import ValidationMessage


class PropertyValidationMessage(ValidationMessage):
    PROPERTY_NAME = 'PropertyName'

    SERIALIZABLE = (
        *ValidationMessage.SERIALIZABLE,
        (PROPERTY_NAME, 'property_name')
    )

    def __init__(self, property_name: str):
        super().__init__()
        self._property_name = property_name

    @property
    def property_name(self):
        return self._property_name

    @property
    def type(self):
        return 'Property'
