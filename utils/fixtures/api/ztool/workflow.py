import pytest

from base.api.ztool.workflows import submit_workflow, get_workflow, send_submitted_workflow_to_grading, grade_workflow, \
    approve_workflow
from models.users.role import SupportedRoles
from models.ztool.answer import Answers
from models.ztool.attachment import AnswerFeedbackAttachments, AnswerAttachments
from models.ztool.exercise import Exercises
from models.ztool.workflow import Workflows


@pytest.fixture(scope='function')
def started_workflow(request, learner):
    request_id = learner['request_id']
    workflow_id = learner['workflow_id']
    element_id = learner['element_id']
    answers = request.param.get('answers', []) if hasattr(request, 'param') else []
    exercises = request.param.get('exercises', []) if hasattr(request, 'param') else []
    attachments = request.param.get('attachments', []) if hasattr(request, 'param') else []
    safe_exercises = [Exercises.manager.create(**exercise, element_id=element_id) for exercise in exercises]
    safe_answers = [
        Answers.manager.create(**answer, exercise_id=exercise['exercise_id'], workflow_id=workflow_id)
        for answer, exercise in zip(answers, safe_exercises)
    ]
    safe_attachments = [
        AnswerAttachments.manager.create(**attachment, answer_id=answer['answer_id'])
        for attachment, answer in zip(attachments, safe_answers)
    ]
    return {
        'data': get_workflow(request_id, workflow_id).json(),
        'exercises': safe_exercises,
        'answers': safe_answers,
        'attachments': safe_attachments,
        SupportedRoles.LEARNER: learner,
    }


@pytest.fixture(scope='function')
def submitted_workflow(request, started_workflow, learner, author, observer, instructor):
    request_id = learner['request_id']
    workflow_id = learner['workflow_id']

    feedback_attachments = request.param.get('feedback_attachments', []) if hasattr(request, 'param') else []
    safe_feedback_attachments = [
        AnswerFeedbackAttachments.manager.create(**attachment, answer_id=answer['answer_id'])
        for attachment, answer in zip(feedback_attachments, started_workflow['answers'])
    ]

    submit_workflow(request_id, workflow_id)
    return {
        **started_workflow,
        'data': get_workflow(request_id, workflow_id).json(),
        'feedback_attachments': safe_feedback_attachments,
        SupportedRoles.AUTHOR: author,
        SupportedRoles.OBSERVER: observer,
        SupportedRoles.INSTRUCTOR: instructor
    }


@pytest.fixture(scope='function')
def in_grade_workflow(submitted_workflow, author, learner, observer, instructor):
    send_submitted_workflow_to_grading(author['request_id'])
    return {
        **submitted_workflow,
        'data': get_workflow(learner['request_id'], learner['workflow_id']).json(),
        SupportedRoles.AUTHOR: author,
        SupportedRoles.OBSERVER: observer,
        SupportedRoles.INSTRUCTOR: instructor
    }


@pytest.fixture(scope='function')
def graded_workflow(in_grade_workflow, instructor, observer):
    payload = Workflows.manager.to_json
    grade_workflow(instructor['request_id'], instructor['workflow_id'], payload)
    return {
        **in_grade_workflow,
        'data': get_workflow(instructor['request_id'], instructor['workflow_id']).json(),
        SupportedRoles.INSTRUCTOR: instructor,
        SupportedRoles.OBSERVER: observer
    }


@pytest.fixture(scope='function')
def approved_workflow(graded_workflow, observer):
    approve_workflow(observer['request_id'], observer['workflow_id'])
    return {
        **graded_workflow,
        'data': get_workflow(observer['request_id'], observer['workflow_id']).json()
    }
