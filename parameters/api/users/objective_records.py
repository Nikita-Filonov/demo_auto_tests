import uuid

from base.api.users.objectives.objective_records import get_objective_records, get_objective_record, \
    get_objective_records_query

objective_record_id = uuid.uuid4()

objective_record_methods = [
    {'method': get_objective_records, 'args': (), 'key': 'objective_records.get_objective_records'},
    {'method': get_objective_record, 'args': (objective_record_id,), 'key': 'objective_records.get_objective_record'},
    {'method': get_objective_records_query, 'args': ('?skip=0&take=10&requireTotalCount=true',),
     'key': 'objective_records.get_objective_records_query'},
]
