import requests

import settings

if settings.ALLURE_ENDPOINT is None:
    raise NotImplementedError(
        'We could not find "ALLURE_ENDPOINT" variable in your environment. '
        'It is necessary to send slack notification'
    )

ALLURE_API = settings.ALLURE_ENDPOINT + '/api'
ALLURE_USER = {
    "username": settings.ALLURE_USERNAME,
    "password": settings.ALLURE_PASSWORD,
    "grant_type": "password",
    "scope": "openid"
}


def get_allure_token(user: dict = None) -> str:
    payload = user or ALLURE_USER
    response = requests.post(ALLURE_API + '/uaa/oauth/token', data=payload)

    try:
        return response.json()['access_token']
    except KeyError:
        raise NotImplementedError(
            'Are you sure "ALLURE_USERNAME", "ALLURE_PASSWORD" exists in your environment? '
            f'Allure respond with error: {response.status_code}, {response.content}'
        )


def headers(user: dict = None):
    token = get_allure_token(user)
    return {'Authorization': f'Bearer {token}'}
