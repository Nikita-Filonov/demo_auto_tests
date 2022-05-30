import uuid
from datetime import datetime
from typing import Optional

from models_manager import Field, Model

from base.api.ztool.answers import create_answer
from base.api.ztool.launch import get_launch
from models.users.role import SupportedRoles
from settings import ZTOOL_DB_NAME
from utils.utils import random_string


class Answers(Model):
    database = ZTOOL_DB_NAME
    identity = 'answer_id'

    answer_id = Field(default=uuid.uuid4, json='id', category=str)
    exercise_id = Field(default=uuid.uuid4, json='exerciseId', category=str)
    workflow_id = Field(default=uuid.uuid4, json='workflowId', category=str)
    text = Field(default=random_string, null=True, json='text', category=Optional[str])
    feedback = Field(default=random_string, null=True, json='feedback', category=Optional[str])
    score = Field(default=1, null=True, json='score', category=Optional[int])
    attachments = Field(json='attachments', only_json=True, category=list)
    feedback_attachments = Field(json='feedbackAttachments', only_json=True, category=list)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    modified = Field(default=datetime.now, category=str)
    modified_by_user_id = Field(default=uuid.uuid4, category=str)

    def __str__(self):
        return f'<Answer {self.answer_id}>'


def get_default_answer():
    """Returns answer with default properties"""
    launch = get_launch(SupportedRoles.AUTHOR)
    answer_payload = Answers.manager.to_json
    return create_answer(launch['request_id'], answer_payload).json()['id']
