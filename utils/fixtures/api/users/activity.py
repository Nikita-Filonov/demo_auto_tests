from typing import Tuple

import pytest
from alms_integration import create_activity

from models.users.activity import Activities, TextActivity


@pytest.fixture(scope='function')
def activity_function(request) -> Tuple[Activities, dict]:
    activity_model: Activities = request.param if hasattr(request, 'param') else TextActivity
    activity_payload = activity_model.manager.to_json
    return activity_model, create_activity(activity_payload).json()


@pytest.fixture(scope='class')
def activity_class(request) -> Tuple[Activities, dict]:
    activity_model: Activities = request.param if hasattr(request, 'param') else TextActivity
    activity_payload = Activities.manager.to_json
    return activity_model, create_activity(activity_payload).json()
