from utils.api.validation.messages.property_validation_message import PropertyValidationMessage


class CantModifyPropertyValidationMessage(PropertyValidationMessage):
    def __init__(self, property_name: str):
        super().__init__(property_name)

        self.parameters = {'property': property_name}

    @property
    def type(self):
        return 'CantModify'

    @property
    def format(self):
        return '{0} cannot be modified'
