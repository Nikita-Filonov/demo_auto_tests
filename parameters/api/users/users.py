import uuid

from base.api.users.users.user_checks import is_user_created, is_user_updated
from base.api.users.users.users import get_users, get_user, create_user, update_user
from models.users.user import Users

user_payload = Users
user_id = uuid.uuid4()

user_methods = [
    {'method': get_users, 'args': (), 'key': 'users.get_users'},
    {'method': get_user, 'args': (user_id,), 'key': 'users.get_user'},
    {'method': create_user, 'args': (user_payload,), 'key': 'users.create_user'},
    {'method': update_user, 'args': (user_id, user_payload,), 'key': 'users.update_user'},
    {'method': is_user_created, 'args': (user_id,), 'key': 'users.is_user_created'},
    {'method': is_user_updated, 'args': (user_id,), 'key': 'users.is_user_updated'},
]
