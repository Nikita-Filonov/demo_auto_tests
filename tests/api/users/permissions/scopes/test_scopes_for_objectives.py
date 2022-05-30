from http import HTTPStatus

import allure
import pytest
from alms_integration import create_objective

from base.api.base import BaseAPI
from base.api.users.objectives.objective_checks import is_objective_created, is_objective_updated
from base.api.users.objectives.objectives import get_objectives, get_objective, update_objective, get_objectives_query
from models.users.objective import Objectives, get_default_objective
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
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_OBJECTIVES.value)
@pytest.mark.parametrize('user_with_permissions_class', [Objectives.SCOPE], indirect=['user_with_permissions_class'])
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForObjectivesApi(BaseAPI):
    exclude = ['objectives', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    objective_id = cache_callable(get_default_objective)
    objective_payload = Objectives

    @allure.id("1817")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1272', name='[MailSender] 500 error when creating user')
    @allure.title('Check permissions for "Objectives" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_objectives, 'args': (), 'response': HTTPStatus.OK},
        {'method': get_objective, 'args': (objective_id,), 'response': HTTPStatus.OK},
        {'method': create_objective, 'args': (objective_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': update_objective, 'args': (objective_id, objective_payload), 'response': HTTPStatus.ACCEPTED},
        {'method': is_objective_created, 'args': (objective_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_objective_updated, 'args': (objective_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': get_objectives_query, 'args': ('?skip=0&take=10&requireTotalCount=true',),
         'response': HTTPStatus.OK},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_objectives_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
