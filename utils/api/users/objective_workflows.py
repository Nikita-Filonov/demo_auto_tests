from http import HTTPStatus

from assertions import assert_attr, validate_json, assert_response_status

from base.api.users.objectives.objective_workflows import get_objective_workflow
from models.users.objective_workflow import ObjectiveWorkflows, ObjectiveWorkflowStates
from models.users.role import SupportedRoles


def check_objective_workflow_state(fixture: dict, expected_state: ObjectiveWorkflowStates):
    """
    :param fixture: any fixture that running through workflow states
    :param expected_state: expected workflow state
    :return:

    Wrapper around action for checking objective workflow state
    """
    objective_workflow_id = fixture[SupportedRoles.LEARNER]['workflow_id']
    response = get_objective_workflow(objective_workflow_id)
    json_response = response.json()

    assert_response_status(response.status_code, HTTPStatus.OK)
    assert_attr(json_response['state'], expected_state.value, ObjectiveWorkflows.state.json)
    assert_attr(json_response['id'], objective_workflow_id, ObjectiveWorkflows.objective_workflow_id.json)
    assert_attr(json_response['objectiveId'], fixture[SupportedRoles.LEARNER]['objective_id'],
                ObjectiveWorkflows.objective_id.json)
    validate_json(json_response, ObjectiveWorkflows.manager.to_schema)
