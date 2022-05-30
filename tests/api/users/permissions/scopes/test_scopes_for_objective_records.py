from http import HTTPStatus

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.objectives.objective_records import get_objective_records, get_objective_record, \
    get_objective_records_query
from models.users.objective_records import ObjectiveRecords, get_default_objective_record
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
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_OBJECTIVE_RECORDS.value)
@pytest.mark.parametrize(
    'user_with_permissions_class',
    [ObjectiveRecords.SCOPE],
    indirect=['user_with_permissions_class']
)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForObjectiveRecordsApi(BaseAPI):
    exclude = ['objective_records', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    objective_record_id = cache_callable(get_default_objective_record)

    @allure.id("1829")
    @allure.title('Check permissions for "ObjectiveRecords" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_objective_records, 'args': (), 'response': HTTPStatus.OK},
        {'method': get_objective_record, 'args': (objective_record_id,), 'response': HTTPStatus.OK},
        {'method': get_objective_records_query, 'args': ('?skip=0&take=10&requireTotalCount=true',),
         'response': HTTPStatus.OK},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_objective_records_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
