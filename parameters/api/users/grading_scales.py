import uuid

from base.api.users.grading_scales.grading_scales import get_grading_scales, create_grading_scale, update_grading_scale, \
    delete_grading_scale, get_grading_scale, get_grading_scales_query
from base.api.users.grading_scales.grading_scales_checks import is_grading_scale_created, is_grading_scale_deleted, \
    is_grading_scale_updated
from models.users.grading_scale import GradingScales

grading_scale_id = uuid.uuid4()
grading_scale_payload = GradingScales

grading_scales_methods = [
    {'method': get_grading_scales, 'args': (), 'key': 'grading_scales.get_grading_scales'},
    {'method': create_grading_scale, 'args': (grading_scale_payload,), 'key': 'grading_scales.create_grading_scale'},
    {'method': update_grading_scale, 'args': (grading_scale_id, grading_scale_payload,),
     'key': 'grading_scales.update_grading_scale'},
    {'method': delete_grading_scale, 'args': (grading_scale_id,), 'key': 'grading_scales.delete_grading_scale'},
    {'method': get_grading_scale, 'args': (grading_scale_id,), 'key': 'grading_scales.get_grading_scale'},
    {'method': is_grading_scale_created, 'args': (grading_scale_id,), 'key': 'grading_scales.is_grading_scale_created'},
    {'method': is_grading_scale_deleted, 'args': (grading_scale_id,), 'key': 'grading_scales.is_grading_scale_deleted'},
    {'method': is_grading_scale_updated, 'args': (grading_scale_id,), 'key': 'grading_scales.is_grading_scale_updated'},
    {'method': get_grading_scales_query, 'args': ('?skip=0&take=10&requireTotalCount=true',),
     'key': 'grading_scales.get_grading_scales_query'}
]
