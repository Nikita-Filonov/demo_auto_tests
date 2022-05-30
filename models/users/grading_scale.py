import uuid
from datetime import datetime

from models_manager import Field, Model

from base.api.users.grading_scales.grading_scales import create_grading_scale
from parameters.api.users.grades import DEFAULT_GRADES
from settings import DEFAULT_TENANT, USERS_DB_NAME
from utils.utils import random_string


class GradingScales(Model):
    SCOPE = [
        {'name': 'GradingScale.Read', 'scope': None, 'scopeType': None},
        {'name': 'GradingScale.Delete', 'scope': None, 'scopeType': None},
        {'name': 'GradingScale.Update', 'scope': None, 'scopeType': None},
        {'name': 'GradingScale.Create', 'scope': None, 'scopeType': None},
    ]
    database = USERS_DB_NAME
    identity = 'grading_scale_id'

    grading_scale_id = Field(default=uuid.uuid4, json='id', category=str)
    name = Field(default=random_string, json='name', category=str)
    grades = Field(default=DEFAULT_GRADES, json='grades', category=list, only_json=True)
    number_of_grades = Field(json='numberOfGrades', category=int, only_json=True)
    max_score = Field(json='maxScore', category=int, only_json=True)
    tenant_id = Field(default=DEFAULT_TENANT['id'], json='tenantId', category=str, is_related=True, optional=True)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    created_on_behalf_of_user_id = Field(default=uuid.uuid4, category=str)
    modified = Field(default=datetime.now, category=str)
    modified_by_user_id = Field(default=uuid.uuid4, category=str)
    modified_on_behalf_of_user_id = Field(default=uuid.uuid4, category=str)
    removed = Field(default=datetime.now, category=str)
    removed_by_user_id = Field(default=uuid.uuid4, category=str)
    removed_on_behalf_of_user_id = Field(default=uuid.uuid4, category=str)

    def __str__(self):
        return f'<GradingScale {self.grading_scale_id}, {self.name}>'


def get_default_grading_scale():
    """Returns grading scale with default properties"""
    payload = GradingScales.manager.to_json
    return create_grading_scale(payload).json()[GradingScales.grading_scale_id.json]
