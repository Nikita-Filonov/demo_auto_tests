import uuid
from datetime import datetime

from models_manager import Field, Model

from models.users.objective import get_default_objective
from settings import DEFAULT_TENANT, USERS_DB_NAME, DEFAULT_USER


class ObjectiveRecords(Model):
    SCOPE = [
        {'name': 'ObjectiveRecord.Read', 'scope': None, 'scopeType': None},
        {'name': 'ObjectiveRecord.Read', 'scope': 'Self', 'scopeType': 'User'},
        {'name': 'ObjectiveRecord.Create', 'scope': 'Self', 'scopeType': 'User'},
    ]
    database = USERS_DB_NAME
    identity = 'objective_record_id'

    objective_record_id = Field(default=uuid.uuid4, json='id', category=str)
    objective_id = Field(
        default=get_default_objective,
        json='objectiveId',
        is_related=True,
        category=str,
        optional=True
    )
    user_id = Field(default=DEFAULT_USER['id'], json='userId', is_related=True, category=str, optional=True)
    score = Field(default=1, json='score', category=int)
    progress = Field(default=1, json='progress', category=int)
    max_score = Field(default=1, json='maxScore', category=int)
    normalized_score = Field(default=1, json='normalizedScore', category=int)
    state = Field(default=1, json='state', is_related=True, category=int)
    tenant_id = Field(default=DEFAULT_TENANT['id'], json='tenantId', is_related=True, optional=True)
    started = Field(default=datetime.now, json='started', category=str)
    submitted = Field(default=datetime.now, json='submitted', category=str)
    finished = Field(default=datetime.now, json='finished', category=str)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    created_on_behalf_of_user_id = Field(default=uuid.uuid4, category=str)


def get_default_objective_record():
    """Returns objective record with default properties"""
    return ObjectiveRecords.manager.create(as_json=False).objective_record_id.value
