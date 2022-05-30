from http import HTTPStatus

import allure
import pytest
from alms_integration import create_activity

from base.api.base import BaseAPI
from base.api.users.activities.activities import get_activity, get_activities, update_activity
from base.api.users.activities.activity_checks import is_activity_created, is_activity_updated
from models.users.activity import Activities, get_default_activity, TextActivity
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.api.users.permissions import PermissionsStory
from utils.api.users.common import Endpoint
from utils.api.users.permissions import make_methods_payload_for_permissions, EXCLUDE_PERMISSIONS_ENDPOINTS, \
    check_permissions_for_entity
from utils.formatters.parametrization import to_method_param
from utils.utils import cache_callable


@pytest.mark.api
@pytest.mark.permissions
@pytest.mark.permissions_scopes
@allure.epic('Core LMS')
@allure.feature('Permissions')
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_ACTIVITIES.value)
@pytest.mark.parametrize('user_with_permissions_class', [Activities.SCOPE], indirect=['user_with_permissions_class'])
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForActivitiesApi(BaseAPI):
    exclude = ['activities', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    activity_id = cache_callable(get_default_activity)
    activity_payload = TextActivity

    @allure.id("1819")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1272', name='[MailSender] 500 error when creating user')
    @allure.title('Check permissions for "Activities" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_activity, 'args': (activity_id,), 'response': HTTPStatus.OK},
        {'method': get_activities, 'args': (), 'response': HTTPStatus.OK},
        {'method': create_activity, 'args': (activity_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': update_activity, 'args': (activity_id, activity_payload), 'response': HTTPStatus.ACCEPTED},
        {'method': is_activity_created, 'args': (activity_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_activity_updated, 'args': (activity_id,), 'response': HTTPStatus.NOT_FOUND},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_activities_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
