import uuid

from alms_integration import create_activity

from base.api.users.activities.activities import get_activities, get_activity, update_activity
from base.api.users.activities.activity_checks import is_activity_created, is_activity_updated
from models.users.activity import Activities

activity_id = uuid.uuid4()
activity_payload = Activities

activity_methods = [
    {'method': get_activities, 'args': (), 'key': 'activities.get_activities'},
    {'method': get_activity, 'args': (activity_id,), 'key': 'activities.get_activity'},
    {'method': create_activity, 'args': (activity_payload,), 'key': 'activities.create_activity'},
    {'method': update_activity, 'args': (activity_id, activity_payload), 'key': 'activities.update_activity'},
    {'method': is_activity_created, 'args': (activity_id,), 'key': 'activities.is_activity_created'},
    {'method': is_activity_updated, 'args': (activity_id,), 'key': 'activities.is_activity_updated'},
]
