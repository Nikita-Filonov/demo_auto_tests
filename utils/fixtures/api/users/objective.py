import pytest
from alms_integration import create_objective, create_objective_access, get_objective_workflow_aggregate

from models.users.objective import Objectives
from models.users.objective_access import ObjectiveAccesses


@pytest.fixture(scope='function')
def objective_function():
    objective_payload = Objectives.manager.to_json
    return create_objective(objective_payload).json()


@pytest.fixture(scope='class')
def objective_class(activity_class):
    _, activity = activity_class
    objective = Objectives(**{Objectives.activity_id.json: activity['id']})
    return create_objective(objective.manager.to_json).json()


@pytest.fixture(scope='function')
def objective_access():
    objective_access_payload = ObjectiveAccesses.manager.to_json
    return create_objective_access(objective_access_payload).json()


@pytest.fixture(scope='function')
def objective_workflow_aggregate(objective_access):
    return get_objective_workflow_aggregate(objective_access['objectiveId']).json()
