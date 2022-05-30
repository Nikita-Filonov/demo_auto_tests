import uuid
from datetime import datetime

from models_manager import Field, Model

from models.utils.utils import get_email
from settings import DEFAULT_USER, IDENTITY_DB_NAME
from utils.utils import random_string, memoize


@memoize(2)
def username_and_email():
    """
    For creating account we need same username and email.
    This function caches up to 2 emails
    """
    return get_email()


class AspNetUsers(Model):
    database = IDENTITY_DB_NAME
    identity = 'Id'
    email = get_email()

    Id = Field(default=uuid.uuid4, json='id', category=str)
    UserName: str = Field(default=username_and_email, json='username')
    NormalizedUserName: str = Field(default=random_string)
    Email: str = Field(default=username_and_email, json='email')
    NormalizedEmail: str = Field(default=random_string)
    EmailConfirmed: bool = Field(default=True)
    PasswordHash: str = Field(default=None, null=True)
    SecurityStamp: str = Field(default=None, null=True)
    ConcurrencyStamp: datetime = Field(default=datetime.now)
    PhoneNumber: str = Field(default=None, null=True)
    PhoneNumberConfirmed: bool = Field(default=True)
    TwoFactorEnabled: bool = Field(default=False)
    LockoutEnd: datetime = Field(default=None, null=True)
    LockoutEnabled: bool = Field(default=True)
    AccessFailedCount: int = Field(default=0)

    LastName: str = Field(default=random_string, only_json=True, json='lastName')
    Password = Field(default=DEFAULT_USER['password'], only_json=True, json='password')

    def __str__(self):
        return f'<AspNetUser {self.Id}, {self.Email}>'
