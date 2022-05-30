import os

from utils.allure.api.launches import get_allure_launches
from utils.formatters.slack import result_message, get_result_status
from utils.slack.messages import send_slack_message


def notify_tests_result():
    pipeline_id = os.environ.get('CI_PIPELINE_ID')
    launch_id = get_allure_launches()['content'][0]['id']
    failed, collected = get_result_status()

    markup = result_message(launch_id, pipeline_id, failed, collected)
    send_slack_message(**markup)


if __name__ == '__main__':
    notify_tests_result()
