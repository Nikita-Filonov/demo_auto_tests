import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from models_manager import Field, Model

from models.ztool.element import get_default_element
from settings import ZTOOL_DB_NAME, DEFAULT_USER
from utils.utils import random_string


class WorkflowStates(Enum):
    IN_PROGRESS = 1
    SUBMITTED = 2
    IN_GRADING = 3
    RETURNED = 4
    REGRADING = 5
    GRADED = 6
    GRADING_APPROVED = 7
    FINISHED = 8


class WorkflowDatetime(Enum):
    """
    Abstract:
    WorkflowState = WorkflowModel.DateTimeColumns
    """
    SUBMITTED = 'submitted'
    FINISHED = 'finished'
    GRADED = 'graded'
    GRADE_APPROVED = 'grade_approved'


class Workflows(Model):
    database = ZTOOL_DB_NAME
    identity = 'workflow_id'

    workflow_id = Field(default=uuid.uuid4, json='id', category=str)
    user_id = Field(default=DEFAULT_USER['id'], json='userId', category=str)
    element_id = Field(default=get_default_element, json='elementId', category=str)
    finished_user_id = Field(default=uuid.uuid4, category=str, null=True)
    grade_approved_user_id = Field(default=uuid.uuid4, category=str, null=True)
    submitted_user_id = Field(default=uuid.uuid4, category=str, null=True)
    in_grading_user_id = Field(default=uuid.uuid4, category=str, null=True)
    graded_user_id = Field(default=uuid.uuid4, category=str, null=True)
    state = Field(default=WorkflowStates.IN_PROGRESS.value, json='state', category=Optional[int], null=True)
    feedback = Field(default=random_string, json='feedback', category=Optional[str], null=True)
    grade = Field(default=random_string, json='grade', category=Optional[str], null=True)
    bonus = Field(default=0, json='bonus', category=Optional[int], null=True)
    due = Field(default=datetime.now, json='dueDate', category=Optional[str], null=True)
    graded = Field(default=datetime.now, json='gradedDate', category=Optional[str], null=True)
    finished = Field(default=datetime.now, json='finishedDate', category=Optional[str], null=True)
    grade_approved = Field(default=datetime.now, json='gradeApprovedDate', category=Optional[str], null=True)
    in_grading = Field(default=datetime.now, category=Optional[str], null=True)
    available = Field(default=datetime.now, json='availabilityDate', category=Optional[str], null=True)
    submitted = Field(default=datetime.now, json='submissionDate', category=Optional[str], null=True)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    modified = Field(default=datetime.now, category=str)
    modified_by_user_id = Field(default=uuid.uuid4, category=str)

    def __str__(self):
        return f'<Workflow {self.workflow_id}>'
