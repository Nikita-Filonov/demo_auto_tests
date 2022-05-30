import logging
from typing import List

from slack.errors import SlackApiError

from settings import SLACK_CHANNEL
from utils.slack.client import client


def send_slack_message(message: str, blocks: List[dict]):
    try:
        client.chat_postMessage(channel=SLACK_CHANNEL, text=message, blocks=blocks)
    except SlackApiError as error:
        logging.error(f'Error happened while sending slack message: {error}')
