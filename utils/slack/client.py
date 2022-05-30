from slack import WebClient

import settings

if settings.SLACK_API_TOKEN is None:
    raise NotImplementedError('We could not send the notification to Slack without "SLACK_API_TOKEN"')

client = WebClient(token=settings.SLACK_API_TOKEN)
