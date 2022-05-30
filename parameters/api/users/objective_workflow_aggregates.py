import uuid

from base.api.users.objectives.objective_workflow_aggregates import get_objective_workflow_aggregates

objective_workflow_aggregate_id = uuid.uuid4()

objective_workflow_aggregate_methods = [
    {
        'method': get_objective_workflow_aggregates,
        'args': (),
        'key': 'objective_workflow_aggregates.get_objective_workflow_aggregates'
    },
]
