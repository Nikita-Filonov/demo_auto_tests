"""
ztool fixtures

As default agreement every entity fixture, should return payload like:
{
    'data': {...} <- entity data,
    'request_id': 'some_id',
    ...
    any other helpful keywords
}
"""

import pytest

from base.api.ztool.answers import create_answer
from base.api.ztool.element import upload_file_to_element
from base.api.ztool.exercises import create_exercise
from base.api.ztool.launch import get_launch
from models.users.role import SupportedRoles
from models.ztool.answer import Answers
from models.ztool.element import get_default_element
from models.ztool.exercise import Exercises

EXCLUDE_FILES = ['some.txt', 'some.json']  # those types files does not supported
ROLES = [SupportedRoles.LEARNER, SupportedRoles.AUTHOR, SupportedRoles.INSTRUCTOR]


@pytest.fixture(scope='function')
def launch(request) -> dict:
    role = request.param if hasattr(request, 'param') else SupportedRoles.LEARNER  # define role for getting token
    return {**get_launch(role), 'role': role.value}


@pytest.fixture(scope='function')
def learner(request) -> dict:
    if not hasattr(request, 'param'):
        return get_launch(SupportedRoles.LEARNER)

    element_id = get_default_element(**request.param['element'])
    return get_launch(SupportedRoles.LEARNER, element_id=element_id)


@pytest.fixture(scope='function')
def author(request, learner) -> dict:
    element_id = learner['element_id']
    workflow_id = learner['workflow_id']
    objective_id = learner['objective_id']

    files = request.param['files'] if hasattr(request, 'param') else []

    author = get_launch(SupportedRoles.AUTHOR, element_id, workflow_id, objective_id)
    request_id = author['request_id']

    for file in files:
        upload_file_to_element(request_id, element_id, file)

    return author


@pytest.fixture(scope='function')
def instructor(learner) -> dict:
    element_id = learner['element_id']
    workflow_id = learner['workflow_id']
    objective_id = learner['objective_id']
    return get_launch(SupportedRoles.INSTRUCTOR, element_id, workflow_id, objective_id)


@pytest.fixture(scope='function')
def observer(learner) -> dict:
    element_id = learner['element_id']
    workflow_id = learner['workflow_id']
    objective_id = learner['objective_id']
    return get_launch(SupportedRoles.OBSERVER, element_id, workflow_id, objective_id)


@pytest.fixture(scope='function')
def exercise(author) -> dict:
    exercise_payload = Exercises.manager.to_json
    exercise_payload['elementId'] = author['element_id']
    author_launch = get_launch(SupportedRoles.AUTHOR, element_id=author['element_id'])
    return {
        'data': create_exercise(author_launch['request_id'], exercise_payload).json(),
        **author
    }


@pytest.fixture(scope='function')
def answer(learner, exercise) -> dict:
    answer_payload = Answers.manager.to_json
    answer_payload['exerciseId'] = exercise['data']['id']
    answer_payload['workflowId'] = learner['workflow_id']
    return {
        'data': create_answer(learner['request_id'], answer_payload).json(),
        'exercise_id': exercise['data']['id'],
        **learner
    }
