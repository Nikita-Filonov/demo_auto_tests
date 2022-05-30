import re
from typing import Optional

import allure
from alms_integration import get_objective_workflow_aggregate, start_objective_workflow
from api_manager import post, get

from base.api.base import Z_TOOL_API_URL
from base.api.users.objectives.objective_accesses import get_objective_access
from base.api.users.objectives.objectives import get_objective, get_objective_resource_link
from models.users.objective_access import get_default_objective_access
from models.users.objective_workflow import ObjectiveWorkflows
from models.users.role import SupportedRoles
from settings import Z_TOOL_API


def get_launch_request(request_id, user=None):
    with allure.step(f'Getting launch request with id "{request_id}"'):
        return get(Z_TOOL_API_URL + f'/launch-requests/{request_id}', user=user)


def create_launch(element_id, id_token, role=SupportedRoles.AUTHOR.value) -> dict:
    with allure.step(f'Creating launch for role "{role}"'):
        response = post(Z_TOOL_API + f'/launch/{element_id}', data={'id_token': id_token})

    redirect_url = response.history[0].headers['Location']
    request_id = re.findall(rf"/{role.lower()}/([A-Za-z0-9\-]+)", redirect_url)[0]
    return {'request_id': request_id}


def get_launch(role: SupportedRoles = SupportedRoles.LEARNER,
               element_id: Optional[str] = None,
               workflow_id: Optional[str] = None,
               objective_id: Optional[str] = None,
               user: Optional[dict] = None) -> dict:
    """
    Returns launch with default properties.
    Method can take role, this will influence token generation
    """
    objective_access = get_objective_access(get_default_objective_access()).json()
    objective_workflow_aggregate = get_objective_workflow_aggregate(objective_access['objectiveId']).json()
    objective = get_objective(objective_workflow_aggregate['objective']['id']).json()
    safe_objective_id = objective_id or objective['id']
    safe_element_id = element_id or objective['activity']['toolResourceId']  # need this to create launch

    # before generating token and getting request_id, we have to start objective workflow
    start_objective_workflow_payload = {'objectiveWorkflowAggregateId': objective_workflow_aggregate['id']}
    start_objective_workflow(start_objective_workflow_payload)

    safe_workflow_id = workflow_id or ObjectiveWorkflows.manager.get(
        objective_id=safe_objective_id)['objective_workflow_id']
    # getting token for given role
    token = get_objective_resource_link(safe_objective_id, role.value, safe_workflow_id, user).json()['token']
    # creating launch and getting request_id from redirect
    request_id = create_launch(safe_element_id, token, role.value)['request_id']
    return {
        'element_id': safe_element_id,
        'request_id': request_id,
        'workflow_id': safe_workflow_id,
        'objective_id': safe_objective_id,
        'objective_workflow_aggregate_id': objective_workflow_aggregate['id']
    }
