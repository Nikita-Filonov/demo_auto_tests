from http import HTTPStatus
from typing import Optional

from assertions import assert_attr, assert_response_status, validate_json
from requests import Response

from models.ztool.workflow import Workflows, WorkflowStates


def check_workflow_state(workflow_response: Response,
                         fixture: dict,
                         state: WorkflowStates,
                         payload: Optional[dict] = None):
    """
    :param workflow_response: Workflow response which should contains info about workflow. For example
    json of such response might look like:
    {
        'id': 'some-uuid',
        'state': 5,
        'elementId': 'another-uuid'
        ...
    }

    :param fixture: This should be any fixture that contains workflow_id, element_id.
    Any fixture because workflow_id, element_id always the same, even for different
    roles. Difference only in request_id, but this not the point to check, in that case.

    :param state: This should be integer number of expected state, which workflow should have.
    For more info about workflow states go to /models/ztool/workflow.py, and chek model ``Workflow``

    :param payload: Optional payload, can be passed if workflow ``feedback``, or other properties
    was changed
    :return:
    """
    workflow_json_response = workflow_response.json()

    assert_response_status(workflow_response.status_code, HTTPStatus.OK)
    assert_attr(workflow_json_response['id'], fixture['workflow_id'], Workflows.workflow_id.json)
    assert_attr(workflow_json_response['state'], state.value, Workflows.state.json)
    assert_attr(workflow_json_response['elementId'], fixture['element_id'], Workflows.element_id.json)

    if payload:
        assert_attr(workflow_json_response['feedback'], payload['feedback'], Workflows.feedback.json)

    validate_json(workflow_json_response, Workflows.manager.to_schema)
