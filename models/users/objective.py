from alms_integration import Objectives as ObjectivesLib, create_objective
from models_manager import Field, Model

from models.users.activity import get_default_activity
from settings import USERS_DB_NAME


class Objectives(ObjectivesLib):
    database = USERS_DB_NAME

    activity_id = Field(default=get_default_activity, json='activityId', is_related=True, category=str, optional=True)


def get_default_objective(**kwargs):
    """Returns objective with default properties"""
    payload = Objectives.manager.to_json
    return create_objective({**payload, **kwargs}).json()['id']


class CreateObjectives(Model):
    database = USERS_DB_NAME
    identity = 'create_objective_id'

    create_objective_id = Field(category=str)


class UpdateObjectives(Model):
    database = USERS_DB_NAME
    identity = 'update_objective_id'

    update_objective_id = Field(category=str)
