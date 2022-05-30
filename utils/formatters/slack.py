import json
from json import JSONDecodeError
from typing import Tuple

from settings import GITLAB, ALLURE_ENDPOINT, LEARNER_URL

FAILED = 'failed'
COLLECTED = 'collected'
RESULT_FILE = 'results.json'


def get_safe_allure_endpoint(endpoint: str):
    """
    Wrapper around allure link. Used to replace second
    domain of the link, which is not resolved by kubernetes network
    """
    return endpoint.replace('.com', '.dev')


def save_result_status(failed: int, collected: int):
    """
    Saving status of test run
    """
    payload = {FAILED: failed, COLLECTED: collected}
    with open(RESULT_FILE, 'w') as file:
        file.write(json.dumps(payload))


def get_result_status() -> Tuple[int, int]:
    """Used to resolve status of job"""
    try:
        result = json.loads(open(RESULT_FILE, 'r').read())
        return result[FAILED], result[COLLECTED]
    except (FileNotFoundError, JSONDecodeError):
        return 0, 0


def result_message(launch_id: str, pipeline_id: str, failed: int, collected: int):
    """
    :return:
    """
    status = 'Failed' if (failed > 0) else 'Success'

    failed_message = f'{failed} of {collected}'
    title = f"Pipeline {status}. Tests {failed_message} failed"
    safe_pipeline_id = pipeline_id or 'Unknown'
    safe_allure_endpoint = get_safe_allure_endpoint(ALLURE_ENDPOINT)
    markup = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"Pipeline {status}",
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Pipeline:*\n"
                            f"<{GITLAB + f'/-/pipelines/{pipeline_id}'}|*#{safe_pipeline_id}*>"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Allure launch:*\n"
                            f"<{safe_allure_endpoint + f'/launch/{launch_id}'}|*#{launch_id}*>"
                },
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Tests:*\n{failed_message} failed"
                },
                {
                    "type": "mrkdwn",
                    "text": F"*Launch domain:*\n<{LEARNER_URL}|{LEARNER_URL}>"
                },
            ]
        }
    ]

    return {'blocks': markup, 'message': title}
