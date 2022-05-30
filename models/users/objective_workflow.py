import uuid
from datetime import datetime
from typing import Optional

from models_manager import Field, Model, FieldGenericEnum

from models.users.objective import get_default_objective
from models.users.objective_records import get_default_objective_record
from settings import DEFAULT_TENANT, USERS_DB_NAME, DEFAULT_USER


class ObjectiveWorkflowStates(FieldGenericEnum):
    IN_PROGRESS = 1
    SUBMITTED = 2
    IN_GRADING = 3
    GRADED = 4
    GRADING_APPROVED = 5
    FINISHED = 6


class ObjectiveWorkflows(Model):
    SCOPE = [
        {'name': 'ObjectiveWorkflow.Read', 'scope': None, 'scopeType': None},
        {'name': 'ObjectiveWorkflow.Delete', 'scope': None, 'scopeType': None},
        {'name': 'ObjectiveWorkflow.Update', 'scope': None, 'scopeType': None},
        {'name': 'ObjectiveWorkflow.Create', 'scope': None, 'scopeType': None},
        {'name': 'ObjectiveWorkflow.Read', 'scope': 'Self', 'scopeType': 'ObjectiveAccess'},
        {'name': 'ObjectiveWorkflow.Update', 'scope': 'Self', 'scopeType': 'ObjectiveAccess'},
        {'name': 'ObjectiveWorkflow.Create', 'scope': 'Self', 'scopeType': 'ObjectiveAccess'},
    ]
    database = USERS_DB_NAME
    identity = 'objective_workflow_id'

    objective_workflow_id = Field(default=uuid.uuid4, json='id', category=str)
    tenant_id = Field(default=DEFAULT_TENANT['id'], json='tenantId', is_related=True, category=str)
    objective_id = Field(default=get_default_objective, json='objectiveId', is_related=True, category=str)
    user_id = Field(default=DEFAULT_USER['id'], json='userId', is_related=True, category=str)
    objective_record_id = Field(default=get_default_objective_record, is_related=True, category=str)
    score = Field(default=1.0, json='score', is_related=True, category=Optional[float], null=True)
    progress = Field(default=1.0, category=Optional[float], null=True)
    max_score = Field(default=1.0, category=Optional[float], null=True)
    normalized_score = Field(default=1.0, category=Optional[float], null=True)
    state = Field(default=1, json='state', category=int, choices=ObjectiveWorkflowStates.to_list())
    started = Field(default=datetime.now, category=str)
    submitted = Field(default=datetime.now, json='submitted', category=Optional[str])
    finished = Field(default=datetime.now, is_related=True, category=str)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    created_on_behalf_of_user_id = Field(default=uuid.uuid4, category=str)
    modified = Field(default=None, null=True, category=str)
    modified_by_user_id = Field(default=None, null=True, category=str)
    modified_on_behalf_of_user_id = Field(default=None, null=True, category=str)
    grade = Field(default=None, null=True, category=str)


def get_default_objective_workflow():
    """Returns objective workflow with default properties"""
    return ObjectiveWorkflows.manager.create(as_json=False).objective_workflow_id.value
