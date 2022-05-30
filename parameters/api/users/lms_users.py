import uuid

from base.api.users.lms_users.lms_users import get_lms_users, get_lms_user, create_lms_user, update_lms_user, \
    get_lms_users_query
from base.api.users.lms_users.lms_users_checks import is_lms_user_updated, is_lms_user_created
from models.users.lms_user import LmsUsers

lms_user_id = uuid.uuid4()
lms_user_payload = LmsUsers

lms_users_methods = [
    {'method': get_lms_users, 'args': (), 'key': 'lms_users.get_lms_users'},
    {'method': get_lms_user, 'args': (lms_user_id,), 'key': 'lms_users.get_lms_user'},
    {'method': create_lms_user, 'args': (lms_user_payload,), 'key': 'lms_users.create_lms_user'},
    {'method': update_lms_user, 'args': (lms_user_id, lms_user_payload), 'key': 'lms_users.update_lms_user'},
    {'method': is_lms_user_created, 'args': (lms_user_id,), 'key': 'lms_users.is_lms_user_created'},
    {'method': is_lms_user_updated, 'args': (lms_user_id,), 'key': 'lms_users.is_lms_user_updated'},
    {'method': get_lms_users_query, 'args': ('?skip=0&take=10&requireTotalCount=true',),
     'key': 'lms_users.get_lms_users_query'}
]
