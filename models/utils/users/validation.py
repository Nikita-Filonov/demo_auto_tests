from models_manager import Model, Field

from utils.api.constants import APIState


class CommandCompletionResultModel(Model):
    url = Field(json='url', category=str)
    completed = Field(json='completed', category=str)
    state = Field(json='state', choices=APIState.to_list(), category=int)
    errors = Field(json='errors', category=dict)


class ValidationResultModel(Model):
    id = Field(json='id', category=str)
    entity_id = Field(json='entityId', category=str)
    created = Field(json='created', category=str)
    completed = Field(json='completed', category=CommandCompletionResultModel)
