import uuid
from datetime import datetime

from models_manager import Field, Model

from models.utils.utils import get_date, get_attachment_name
from parameters.courses.ui.ztool.grades import grade_properties
from settings import PROJECT_ROOT, ZTOOL_DB_NAME
from utils.utils import random_string

COURSE_HTML = open(PROJECT_ROOT + '/parameters/courses/common/course.html').read()


class Grades(Model):
    database = ZTOOL_DB_NAME
    identity = 'grade_id'

    grade_id = Field(default=uuid.uuid4, json='id', category=str)
    element_id = Field(json='elementId', is_related=True, category=str, optional=True)
    name = Field(default=random_string, json='name', category=str)
    max = Field(default=10, json='max', category=int)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    modified = Field(default=datetime.now, category=str)
    modified_by_user_id = Field(default=uuid.uuid4, category=str)

    def __str__(self):
        return f'<Grade {self.grade_id}>'


class Elements(Model):
    database = ZTOOL_DB_NAME
    identity = 'element_id'

    element_id = Field(default=uuid.uuid4, json='id', category=str)
    name = Field(default=random_string, json='name', category=str)
    image_url = Field(default=random_string, null=True, json='imageUrl', category=str)
    textbook = Field(default=COURSE_HTML, null=True, json='textbook', category=str)
    tutor_guideline = Field(default=random_string, null=True, json='tutorGuideline', category=str)
    min_bonus = Field(default=0, json='minBonus', category=int)
    max_bonus = Field(default=10, json='maxBonus', category=int)
    grading_start_date = Field(default=get_date, null=True, json='gradingStartDate', category=str)
    grading_end_date = Field(default=get_date, null=True, json='gradingEndDate', category=str)
    grade_disclosure_date = Field(default=get_date, null=True, json='gradeDisclosureDate', category=str)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    modified = Field(default=datetime.now, category=str)
    modified_by_user_id = Field(default=uuid.uuid4, category=str)

    def __str__(self):
        return f'<Element {self.element_id}>'


def to_element_update_json():
    payload = Elements.manager.to_json
    payload.pop('id', None)

    limit_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    return {
        **payload,
        'gradingStartDate': limit_date,
        'gradingEndDate': limit_date,
        'gradeDisclosureDate': limit_date,
        'grades': [],
    }


def get_default_element(**kwargs) -> str:
    """Returns element with default properties"""
    element_id = Elements.manager.create(as_json=False, **kwargs).element_id.value
    for grade in grade_properties:
        Grades.manager.create(element_id=element_id, **grade)
    return element_id


class ElementFiles(Model):
    url = Field(default=random_string, json='url', category=str)
    name = Field(default=get_attachment_name, json='name', category=str)
