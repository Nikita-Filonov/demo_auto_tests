from alms_integration import ObjectiveAccesses as ObjectiveAccessesLib, create_objective_access
from models_manager import Field, Model

from models.users.objective import get_default_objective
from settings import USERS_DB_NAME


class ObjectiveAccesses(ObjectiveAccessesLib):
    database = USERS_DB_NAME

    objective_id = Field(default=get_default_objective, json='objectiveId', category=str)


def get_default_objective_access(**kwargs):
    """Returns objective access with default properties"""
    payload = ObjectiveAccesses.manager.to_json
    return create_objective_access({**payload, **kwargs}).json()['id']


class CreateObjectiveAccesses(Model):
    database = USERS_DB_NAME
    identity = 'create_objective_access_id'

    create_objective_access_id = Field(category=str)


class DeleteObjectiveAccesses(Model):
    database = USERS_DB_NAME
    identity = 'delete_objective_access_id'

    delete_objective_access_id = Field(category=str)
