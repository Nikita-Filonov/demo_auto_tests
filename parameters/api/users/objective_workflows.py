import uuid

from alms_integration import start_objective_workflow, get_objective_workflows

from base.api.users.objectives.objective_workflows import get_objective_workflow, \
    get_started_objective_workflow, get_started_objective_workflows, submit_objective_workflow, \
    get_submitted_objective_workflow, get_submitted_objective_workflows
from models.users.objective_workflow import ObjectiveWorkflows

objective_workflow_id = uuid.uuid4()
objective_workflow_payload = ObjectiveWorkflows

objective_workflow_methods = [
    {
        'method': get_objective_workflows,
        'args': (),
        'key': 'objective_workflows.get_objective_workflows'
    },
    {
        'method': get_objective_workflow,
        'args': (objective_workflow_id,),
        'key': 'objective_workflows.get_objective_workflow'
    },
    {
        'method': start_objective_workflow,
        'args': (objective_workflow_payload,),
        'key': 'objective_workflows.start_objective_workflow'
    },
    {
        'method': get_started_objective_workflow,
        'args': (objective_workflow_id,),
        'key': 'objective_workflows.get_started_objective_workflow'
    },
    {
        'method': get_started_objective_workflows,
        'args': (),
        'key': 'objective_workflows.get_started_objective_workflows'
    },
    {
        'method': submit_objective_workflow,
        'args': (objective_workflow_payload,),
        'key': 'objective_workflows.submit_objective_workflow'
    },
    {
        'method': get_submitted_objective_workflow,
        'args': (objective_workflow_id,),
        'key': 'objective_workflows.get_submitted_objective_workflow'
    },
    {
        'method': get_submitted_objective_workflows,
        'args': (),
        'key': 'objective_workflows.get_submitted_objective_workflows'
    }
]
