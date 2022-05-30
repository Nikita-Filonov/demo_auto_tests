from utils.api.validation.messages.validation_message_format import ValidationMessageFormat


class EntityAlreadyExistsValidationMessage(ValidationMessageFormat):
    message_single_key_format = "{0} with {1} '{2}' already exists"
    message_double_key_format = "{0} with {1} '{2}' and {3} '{4}' already exists"
    message_triple_key_format = "{0} with {1} '{2}', {3} '{4}' and {5} '{6}' already exists"

    message_formats = [message_single_key_format, message_double_key_format, message_triple_key_format]

    def __init__(self, entity_name: str, **kwargs):
        super().__init__(**kwargs)

        self._entity_name = entity_name

    @property
    def type(self):
        return 'EntityAlreadyExists'

    @property
    def parameters(self):
        return {
            "entity": self._entity_name,
            **self._resolve_parameters()
        }
