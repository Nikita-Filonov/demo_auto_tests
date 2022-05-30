from typing import Dict, Union

import pytest
from alms_integration import get_objective_workflow_aggregate, start_objective_workflow

from base.api.ztool.launch import get_launch
from base.api.ztool.workflows import submit_workflow, send_submitted_workflow_to_grading, grade_workflow, \
    approve_workflow, send_approved_workflow_to_finished
from models.users.objective_workflow import ObjectiveWorkflows
from models.users.role import SupportedRoles
from models.ztool.answer import Answers
from models.ztool.attachment import AnswerAttachments, AnswerFeedbackAttachments
from models.ztool.exercise import Exercises
from models.ztool.workflow import Workflows
from parameters.courses.ui.ztool.answers import answers_properties


@pytest.fixture(scope='function')
def started_course_ui(request, course_ui):
    element_id = course_ui['element']['element_id']
    objective_id = course_ui['objective']['objective_id']
    objective_workflow_aggregate = get_objective_workflow_aggregate(objective_id).json()

    start_objective_workflow_payload = {'objectiveWorkflowAggregateId': objective_workflow_aggregate['id']}
    start_objective_workflow(start_objective_workflow_payload)

    workflow_id = ObjectiveWorkflows.manager.get(objective_id=objective_id)['objective_workflow_id']

    learner = get_launch(SupportedRoles.LEARNER, element_id=element_id, objective_id=objective_id,
                         workflow_id=workflow_id)

    answers = request.param.get('answers', []) if hasattr(request, 'param') else []
    answer_attachments = request.param.get('answer_attachments', []) if hasattr(request, 'param') else []

    exercises = Exercises.manager.filter(element_id=element_id)
    safe_answers = [
        Answers.manager.create(**answer, workflow_id=workflow_id, exercise_id=exercise['exercise_id'])
        for answer, exercise in zip(answers, exercises)
    ]

    answers = Answers.manager.filter(workflow_id=workflow_id)
    safe_answer_attachments = [
        AnswerAttachments.manager.create(**attachment, answer_id=answer['answer_id'])
        for answer, attachment in zip(answers, answer_attachments)
    ]

    return {
        **course_ui,
        SupportedRoles.LEARNER: {**learner, 'objective_workflow_aggregate_id': objective_workflow_aggregate['id']},
        'answers': safe_answers,
        'answer_attachments': safe_answer_attachments
    }


@pytest.fixture(scope='function')
def submitted_workflow_ui(request, started_course_ui) -> Dict[Union[SupportedRoles, str], Union[list, dict]]:
    workflow_id = started_course_ui[SupportedRoles.LEARNER]['workflow_id']
    request_id = started_course_ui[SupportedRoles.LEARNER]['request_id']
    element_id = started_course_ui[SupportedRoles.LEARNER]['element_id']

    answers = request.param.get('answers', []) if hasattr(request, 'param') else []
    answer_attachments = request.param.get('answer_attachments', []) if hasattr(request, 'param') else []
    feedback_attachments = request.param.get('feedback_attachments', []) if hasattr(request, 'param') else []

    exercises = Exercises.manager.filter(element_id=element_id)
    safe_answers = [
        Answers.manager.create(**answer, workflow_id=workflow_id, exercise_id=exercise['exercise_id'])
        for answer, exercise in zip(answers, exercises)
    ]

    answers = Answers.manager.filter(workflow_id=workflow_id)
    safe_answer_attachments = [
        AnswerAttachments.manager.create(**attachment, answer_id=answer['answer_id'])
        for answer, attachment in zip(answers, answer_attachments)
    ]

    safe_feedback_attachment = [
        AnswerFeedbackAttachments.manager.create(**attachment, answer_id=answer['answer_id'])
        for answer, attachment in zip(answers, feedback_attachments)
    ]

    submit_workflow(request_id, workflow_id)
    return {
        **started_course_ui,
        'answers': safe_answers,
        'answer_attachments': safe_answer_attachments,
        'feedback_attachments': safe_feedback_attachment
    }


@pytest.fixture(scope='function')
def in_grade_workflow_ui(submitted_workflow_ui):
    element_id = submitted_workflow_ui[SupportedRoles.LEARNER]['element_id']
    objective_id = submitted_workflow_ui[SupportedRoles.LEARNER]['objective_id']
    workflow_id = submitted_workflow_ui[SupportedRoles.LEARNER]['workflow_id']
    author = get_launch(SupportedRoles.AUTHOR, element_id=element_id, objective_id=objective_id,
                        workflow_id=workflow_id)

    answers = Answers.manager.filter(workflow_id=workflow_id)
    send_submitted_workflow_to_grading(author['request_id'])
    return {SupportedRoles.AUTHOR: author, 'answers': answers, **submitted_workflow_ui}


@pytest.fixture(scope='function')
def graded_workflow_ui(request, in_grade_workflow_ui):
    element_id = in_grade_workflow_ui[SupportedRoles.LEARNER]['element_id']
    objective_id = in_grade_workflow_ui[SupportedRoles.LEARNER]['objective_id']
    workflow_id = in_grade_workflow_ui[SupportedRoles.LEARNER]['workflow_id']
    instructor = get_launch(SupportedRoles.INSTRUCTOR, element_id=element_id, objective_id=objective_id,
                            workflow_id=workflow_id)

    answers = Answers.manager.filter(workflow_id=workflow_id, as_json=False)
    instructor_grades = request.param['answers'] if hasattr(request, 'param') else answers_properties

    for answer, grade in zip(answers, instructor_grades):
        answer.manager.update(**grade)

    payload = Workflows.manager.to_json
    grade_workflow(instructor['request_id'], workflow_id, payload)
    return {SupportedRoles.INSTRUCTOR: instructor, 'answers': answers, **in_grade_workflow_ui}


@pytest.fixture(scope='function')
def approved_workflow_ui(graded_workflow_ui):
    element_id = graded_workflow_ui[SupportedRoles.AUTHOR]['element_id']
    objective_id = graded_workflow_ui[SupportedRoles.AUTHOR]['objective_id']
    workflow_id = graded_workflow_ui[SupportedRoles.AUTHOR]['workflow_id']

    request_id = graded_workflow_ui[SupportedRoles.AUTHOR]['request_id']

    observer = get_launch(SupportedRoles.OBSERVER, element_id=element_id, objective_id=objective_id,
                          workflow_id=workflow_id)

    approve_workflow(observer['request_id'], workflow_id)

    send_approved_workflow_to_finished(request_id)

    return {SupportedRoles.OBSERVER: observer, **graded_workflow_ui}
