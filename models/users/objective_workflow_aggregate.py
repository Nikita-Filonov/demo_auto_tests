import uuid
from datetime import datetime
from typing import Optional

from models_manager import Field, Model

from models.users.objective import get_default_objective
from models.users.objective_access import get_default_objective_access
from settings import DEFAULT_TENANT, USERS_DB_NAME, DEFAULT_USER


class ObjectiveWorkflowAggregates(Model):
    SCOPE = [
        {'name': 'ObjectiveWorkflowAggregate.Read', 'scope': 'Self', 'scopeType': 'ObjectiveAccess'},
        {'name': 'ObjectiveWorkflowAggregate.Read', 'scope': None, 'scopeType': None},
        {'name': 'ObjectiveWorkflowAggregate.Delete', 'scope': None, 'scopeType': None},
        {'name': 'ObjectiveWorkflowAggregate.Update', 'scope': None, 'scopeType': None},
        {'name': 'ObjectiveWorkflowAggregate.Create', 'scope': None, 'scopeType': None},
        {'name': 'ObjectiveWorkflowAggregate.Update', 'scope': 'Self', 'scopeType': 'ObjectiveAccess'},
    ]
    database = USERS_DB_NAME
    identity = 'objective_workflow_aggregate_id'

    objective_workflow_aggregate_id = Field(default=uuid.uuid4, json='id')
    tenant_id = Field(default=DEFAULT_TENANT['id'], json='tenantId', is_related=True)
    objective_id = Field(default=get_default_objective, json='objectiveId', is_related=True)
    user_id = Field(default=DEFAULT_USER['id'], json='userId', is_related=True)
    last_objective_workflow_id = Field(
        default=None,
        null=True,
        json='lastObjectiveWorkflow',
        is_related=True,
        category=Optional[str]
    )
    last_objective_record_id = Field(
        default=None,
        null=True,
        json='lastObjectiveRecord',
        is_related=True,
        category=Optional[str]
    )
    objective_access_id = Field(default=get_default_objective_access, null=True)
    availability_date = Field(default=None, null=True, json='availabilityDate', is_related=True, category=Optional[str])
    due_date = Field(default=None, null=True, json='dueDate', is_related=True, category=Optional[str])
    retake = Field(default=False, json='retake', is_related=True, category=bool)
    created = Field(default=datetime.now)
    created_by_user_id = Field(default=uuid.uuid4)
    created_on_behalf_of_user_id = Field(default=uuid.uuid4)
    modified = Field(default=None, null=True)
    modified_by_user_id = Field(default=None, null=True)
    modified_on_behalf_of_user_id = Field(default=None, null=True)


def get_default_objective_workflow_aggregate():
    """Returns objective workflow aggregate with default properties"""
    return ObjectiveWorkflowAggregates.manager.create(as_json=False).objective_workflow_aggregate_id.value
