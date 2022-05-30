import uuid

from alms_integration import create_objective_access

from base.api.users.objectives.objective_accesses import get_objective_access, get_objective_accesses, \
    delete_objective_access
from base.api.users.objectives.objective_accesses_check import is_objective_access_created, is_objective_access_deleted
from models.users.objective_access import ObjectiveAccesses

objective_access_id = uuid.uuid4()
objective_access_payload = ObjectiveAccesses

objective_access_methods = [
    {
        'method': get_objective_accesses,
        'args': (),
        'key': 'objective_accesses.get_objective_accesses'
    },
    {
        'method': get_objective_access,
        'args': (objective_access_id,),
        'key': 'objective_accesses.get_objective_access'
    },
    {
        'method': create_objective_access,
        'args': (objective_access_payload,),
        'key': 'objective_accesses.create_objective_access'
    },
    {
        'method': delete_objective_access,
        'args': (objective_access_id,),
        'key': 'objective_accesses.delete_objective_access'
    },
    {
        'method': is_objective_access_created,
        'args': (objective_access_id,),
        'key': 'objective_accesses.is_objective_access_created'
    },
    {
        'method': is_objective_access_deleted,
        'args': (objective_access_id,),
        'key': 'objective_accesses.is_objective_access_deleted'
    }
]
