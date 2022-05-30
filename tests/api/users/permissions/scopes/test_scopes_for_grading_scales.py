from http import HTTPStatus

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.grading_scales.grading_scales import get_grading_scales, get_grading_scale, create_grading_scale, \
    update_grading_scale, delete_grading_scale
from base.api.users.grading_scales.grading_scales_checks import is_grading_scale_created, is_grading_scale_updated, \
    is_grading_scale_deleted
from models.users.grading_scale import GradingScales, get_default_grading_scale
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
@allure.story(PermissionsStory.PERMISSIONS_SCOPES_FOR_GRADING_SCALES.value)
@pytest.mark.parametrize('user_with_permissions_class', [GradingScales.SCOPE], indirect=['user_with_permissions_class'])
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsForGradingScalesApi(BaseAPI):
    exclude = ['grading_scales', *EXCLUDE_PERMISSIONS_ENDPOINTS]
    grading_scale_id = cache_callable(get_default_grading_scale)
    grading_scale_payload = GradingScales

    @allure.id("4672")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1272', name='[MailSender] 500 error when creating user')
    @allure.title('Check permissions for "GradingScales" model (API)')
    @pytest.mark.parametrize('endpoint', [
        {'method': get_grading_scale, 'args': (grading_scale_id,), 'response': HTTPStatus.OK},
        {'method': get_grading_scales, 'args': (), 'response': HTTPStatus.OK},
        {'method': create_grading_scale, 'args': (grading_scale_payload,), 'response': HTTPStatus.ACCEPTED},
        {'method': update_grading_scale, 'args': (grading_scale_id, grading_scale_payload),
         'response': HTTPStatus.ACCEPTED},
        {'method': delete_grading_scale, 'args': (grading_scale_id,), 'response': HTTPStatus.ACCEPTED},
        {'method': is_grading_scale_created, 'args': (grading_scale_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_grading_scale_deleted, 'args': (grading_scale_id,), 'response': HTTPStatus.NOT_FOUND},
        {'method': is_grading_scale_updated, 'args': (grading_scale_id,), 'response': HTTPStatus.NOT_FOUND},
        *make_methods_payload_for_permissions(*exclude)
    ], ids=to_method_param)
    def test_check_permissions_for_grading_scales_model(self, user_with_permissions_class, endpoint):
        check_permissions_for_entity(Endpoint(**endpoint), user_with_permissions=user_with_permissions_class)
