from typing import Dict

import pytest

from models.users.activity import get_default_activity, Activities
from models.users.objective import Objectives, get_default_objective
from models.users.objective_access import get_default_objective_access
from models.utils.ztool.elements import create_element
from models.ztool.attachment import ElementTextbookAttachments
from models.ztool.element import Elements, Grades
from models.ztool.exercise import Exercises
from parameters.courses.ui.ztool.element import element_properties
from parameters.courses.ui.ztool.exercises import exercises_properties
from parameters.courses.ui.ztool.grades import grade_properties
from settings import Z_TOOL_API


@pytest.fixture(scope='function')
def course_ui(request) -> Dict[str, Dict]:
    """
    Return objective with custom properties

    :param request: run with precondition or use 'element' for add properties

    element_payload: dict with properties from class Elements (precondition=element_properties)
    grades_payload: List(Dict) with properties from class Grades (precondition=exercises_properties)
    exercises_payload: List(Dict) with properties from class Exercises (precondition=grade_properties)

    Example:

    def course_ui() -> dict:
    :return objective:
    {
        'objective': {'objective_id': 'id', 'tenant_id': 'id', 'activity_id': 'id', ...}
        'element': {'element_id': 'id', 'name': 'random name', ...}
        'exercises': [{'exercise_id': 'id', 'element_id': 'id', 'max_score': int, slug: 'order_name', ...}]
    }
    """
    element_payload = request.param['element'] if hasattr(request, 'param') else element_properties
    exercises_payload = request.param['exercises'] if hasattr(request, 'param') else exercises_properties
    grades_payload = request.param['grades'] if hasattr(request, 'param') else grade_properties

    element_id = create_element(element_payload, grades_payload, exercises_payload)

    activity_payload = {
        'toolUrl': Z_TOOL_API + f'/launch/{element_id}',
        'toolResourceId': element_id
    }
    activity_id = get_default_activity(**activity_payload)

    objective_payload = {'activityId': activity_id}
    objective_id = get_default_objective(**objective_payload)

    objective_access_payload = {'objectiveId': objective_id}
    get_default_objective_access(**objective_access_payload)

    ElementTextbookAttachments.manager.create(element_id=element_id)

    objective = Objectives.manager.get(objective_id=objective_id)
    element = Elements.manager.get(element_id=element_id)
    exercises = Exercises.manager.filter(element_id=element_id)
    grades = Grades.manager.filter(element_id=element_id)
    activity = Activities.manager.get(activity_id=activity_id)

    return {
        'objective': objective,
        'element': element,
        'exercises': exercises,
        'grades': grades,
        'activity': activity
    }
