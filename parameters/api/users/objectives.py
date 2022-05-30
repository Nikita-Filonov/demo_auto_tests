import uuid

from alms_integration import create_objective

from base.api.users.objectives.objective_checks import is_objective_created, is_objective_updated
from base.api.users.objectives.objectives import get_objective, get_objectives, update_objective, \
    get_objectives_query
from models.users.objective import Objectives

objective_id = uuid.uuid4()
objective_payload = Objectives

objective_methods = [
    {'method': get_objectives, 'args': (), 'key': 'objectives.get_objectives'},
    {'method': get_objective, 'args': (objective_id,), 'key': 'objectives.get_objective'},
    {'method': create_objective, 'args': (objective_payload,), 'key': 'objectives.create_objective'},
    {'method': update_objective, 'args': (objective_id, objective_payload), 'key': 'objectives.update_objective'},
    {'method': is_objective_created, 'args': (objective_id,), 'key': 'objectives.is_objective_created'},
    {'method': is_objective_updated, 'args': (objective_id,), 'key': 'objectives.is_objective_updated'},
    {'method': get_objectives_query, 'args': ('?skip=0&take=10&requireTotalCount=true',),
     'key': 'objectives.get_objectives_query'}
]
