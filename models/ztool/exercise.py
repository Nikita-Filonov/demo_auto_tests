import uuid
from datetime import datetime
from typing import Optional

from models_manager import Field, Model

from models.ztool.element import get_default_element
from settings import ZTOOL_DB_NAME
from utils.utils import random_string


class Exercises(Model):
    database = ZTOOL_DB_NAME
    identity = 'exercise_id'

    exercise_id = Field(default=uuid.uuid4, json='id', category=str)
    element_id = Field(default=get_default_element, json='elementId', category=str)
    max_score = Field(default=0, json='maxScore', category=int)
    slug = Field(default=random_string, json='slug', category=str)
    group = Field(default=random_string, json='group', category=str)
    order = Field(default=0, json='order', category=int)
    text = Field(default=random_string, json='text', category=str)
    correct_answer = Field(default=random_string, json='correctAnswer', category=Optional[str], null=True)
    tutor_guideline = Field(default=random_string, json='tutorGuideline', category=Optional[str], null=True)
    created: datetime = Field(default=datetime.now)
    created_by_user_id: str = Field(default=uuid.uuid4)
    modified: datetime = Field(default=datetime.now)
    modified_by_user_id: str = Field(default=uuid.uuid4)

    def __str__(self):
        return f'<Exercise {self.element_id}>'
