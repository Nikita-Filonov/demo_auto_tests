import requests

import settings
from utils.allure.api.base import ALLURE_API, headers


def get_allure_launches(size=1, page=0):
    params = {
        'projectId': settings.ALLURE_PROJECT_ID,
        'page': page,
        'size': size,
        'preview': True
    }
    response = requests.get(ALLURE_API + '/rs/launch', params=params, headers=headers())
    assert response.ok, f'Allure respond with error: {response.status_code}, {response.content}'

    return response.json()
