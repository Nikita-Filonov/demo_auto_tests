import uuid
from datetime import datetime

from models_manager import Field, Model

from models.ztool.workflow import WorkflowStates
from settings import ZTOOL_DB_NAME, DEFAULT_USER


class WorkflowTransitions(Model):
    database = ZTOOL_DB_NAME
    identity = 'workflow_transition_id'

    workflow_transition_id = Field(default=uuid.uuid4, json='id', category=str)
    user_id = Field(default=DEFAULT_USER['id'], json='userId', category=str)
    from_state = Field(default=WorkflowStates.IN_PROGRESS.value, json='fromState', category=int)
    to_state = Field(default=WorkflowStates.SUBMITTED.value, json='toState', category=int)
    created = Field(default=datetime.now, category=str)
    workflow_id = Field(default=uuid.uuid4, json='workflowId', category=str)

    def __str__(self):
        return f'<WorkflowTransition {self.workflow_transition_id}>'
