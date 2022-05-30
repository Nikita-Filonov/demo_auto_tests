from utils.api.validation.messages.property_validation_message import PropertyValidationMessage


class StringPropertyIsEmptyValidationMessage(PropertyValidationMessage):
    def __init__(self, property_name: str):
        super().__init__(property_name)

    @property
    def format(self):
        return "{0} is empty"

    @property
    def type(self):
        return "StringPropertyIsEmpty"

    @property
    def parameters(self):
        return {'property': self.property_name}
