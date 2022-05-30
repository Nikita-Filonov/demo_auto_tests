from utils.api.validation.messages.property_validation_message import PropertyValidationMessage


class StringPropertyTooLongValidationMessage(PropertyValidationMessage):
    def __init__(self, property_name: str, limit: int):
        super().__init__(property_name)

        self.parameters = {
            'property': property_name,
            'limit': limit
        }

    @property
    def format(self):
        return "{0} length exceeds {1} symbols"

    @property
    def type(self):
        return "StringPropertyTooLong"
