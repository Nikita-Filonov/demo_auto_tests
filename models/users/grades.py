import uuid

from models_manager import Field, Model

from settings import DEFAULT_TENANT, USERS_DB_NAME
from utils.utils import random_string, random_color, random_number

MIN_NUMBER_OF_GRADES = 2


class Grades(Model):
    database = USERS_DB_NAME
    identity = 'grading_scale_id'

    grade_id = Field(default=uuid.uuid4, category=str)
    tenant_id = Field(default=DEFAULT_TENANT['id'], category=str)
    grading_scale_id = Field(default=uuid.uuid4, category=str)
    max_score = Field(default=random_number, json='maxScore', category=int)
    name = Field(default=random_string, json='name', category=str)
    color = Field(default=random_color, json='color', category=str)

    def __str__(self):
        return f'<Grade {self.grade_id}>'
