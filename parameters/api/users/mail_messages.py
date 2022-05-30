import uuid

from base.api.users.mail_messages.mail_messages import get_mail_messages, get_mail_message, get_mail_messages_query

mail_messages_methods = [
    {'method': get_mail_messages, 'args': (), 'key': 'mail_messages.get_mail_messages'},
    {'method': get_mail_message, 'args': (uuid.uuid4(),), 'key': 'mail_messages.get_mail_message'},
    {'method': get_mail_messages_query, 'args': ('some_query',), 'key': 'mail_messages.get_mail_messages_query'}
]
