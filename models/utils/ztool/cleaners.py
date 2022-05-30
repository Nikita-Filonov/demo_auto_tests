from itertools import tee

from models.utils.utils import clear_log
from models.ztool.answer import Answers
from models.ztool.attachment import AnswerAttachments
from models.ztool.element import Elements, Grades
from models.ztool.exercise import Exercises
from models.ztool.resource_launch import ResourceLaunches
from models.ztool.workflow import Workflows
from models.ztool.workflow_transition import WorkflowTransitions
from settings import DEFAULT_USER


def clear_elements():
    """Clears elements and all related models"""
    users_workflows = Workflows.manager.filter(user_id=DEFAULT_USER['id'], as_json=False)
    workflows, elements = tee(users_workflows)
    safe_workflows = tuple(user_workflow.workflow_id.value for user_workflow in workflows)
    safe_elements = tuple(user_workflow.element_id.value for user_workflow in elements)

    with clear_log(Answers):
        answers = Answers.manager.filter(workflow_id__in=safe_workflows, as_json=False)

        with clear_log(AnswerAttachments):
            safe_answers = tuple(answer.answer_id.value for answer in answers)
            AnswerAttachments.manager.filter(answer_id__in=safe_answers, as_json=False).delete()

        answers.delete()

    with clear_log(Exercises):
        Exercises.manager.filter(element_id__in=safe_elements, as_json=False).delete()

    with clear_log(Grades):
        Grades.manager.filter(element_id__in=safe_elements, as_json=False).delete()

    with clear_log(WorkflowTransitions):
        WorkflowTransitions.manager.filter(workflow_id__in=safe_workflows, as_json=False).delete()

    with clear_log(Workflows):
        users_workflows.delete()

    with clear_log(Elements):
        Elements.manager.filter(element_id__in=safe_elements, as_json=False).delete()


def clear_recourse_launches():
    """Clears resource launches and all related models"""
    with clear_log(ResourceLaunches):
        ResourceLaunches.manager.filter(user_id__in=(DEFAULT_USER['id'],), as_json=False).delete()


if __name__ == '__main__':
    clear_recourse_launches()
    clear_elements()
