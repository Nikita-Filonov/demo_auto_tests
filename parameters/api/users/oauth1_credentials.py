import uuid

from alms_integration import create_oauth1_credentials

from base.api.users.oauth1_credentials.oauth1_credentials import get_oauth1_credentials, get_oauth1_credential, \
    update_oauth1_credential
from base.api.users.oauth1_credentials.oauth1_credentials_checks import is_oauth1_credential_created, \
    is_oauth1_credential_updated
from models.users.oauth1_credentials import Oauth1Credentials

oauth1_credential_id = uuid.uuid4()
oauth1_credential_payload = Oauth1Credentials

oauth1_credential_methods = [
    {
        'method': get_oauth1_credentials,
        'args': (),
        'key': 'oauth1_credentials.get_oauth1_credentials'
    },
    {
        'method': get_oauth1_credential,
        'args': (oauth1_credential_id,),
        'key': 'oauth1_credentials.get_oauth1_credential'
    },
    {
        'method': create_oauth1_credentials,
        'args': (oauth1_credential_payload,),
        'key': 'oauth1_credentials.create_oauth1_credentials'
    },
    {
        'method': update_oauth1_credential,
        'args': (oauth1_credential_id, oauth1_credential_payload,),
        'key': 'oauth1_credentials.update_oauth1_credential'
    },
    {
        'method': is_oauth1_credential_created,
        'args': (oauth1_credential_id,),
        'key': 'oauth1_credentials.is_oauth1_credential_created'
    },
    {
        'method': is_oauth1_credential_updated,
        'args': (oauth1_credential_id,),
        'key': 'oauth1_credentials.is_oauth1_credential_updated'
    },
]
