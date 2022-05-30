from alms_integration import Oauth1Credentials as Oauth1CredentialsLib, create_oauth1_credentials
from models_manager import Field, Model

from settings import USERS_DB_NAME


class Oauth1Credentials(Oauth1CredentialsLib):
    database = USERS_DB_NAME


def get_default_oauth1_credentials():
    """Returns oauth1 credentials with default properties"""
    payload = Oauth1Credentials.manager.to_json
    return create_oauth1_credentials(payload).json()['id']


class CreateOauth1Credentials(Model):
    database = USERS_DB_NAME
    identity = 'create_o_auth1credential_id'

    create_o_auth1credential_id = Field(category=str)


class UpdateOauth1Credentials(Model):
    database = USERS_DB_NAME
    identity = 'update_o_auth1credential_id'

    update_o_auth1credential_id = Field(category=str)
