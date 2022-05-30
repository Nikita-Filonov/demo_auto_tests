import os

import alms_integration.settings
import api_manager.settings
import models_manager.settings
from api_manager import Project

DEBUG = False

RERUNS = 3
RERUNS_DELAY = 2
WAIT_TIMEOUT = 15

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CERT_PATH = PROJECT_ROOT + '/infrastructure/RootCA.crt' if DEBUG \
    else os.environ.get('CERT_PATH', '/etc/ssl/certs/ca-certificates.crt')

USERS_API = os.environ.get('USERS_API', 'https://host.docker.internal:44001')
Z_TOOL_API = os.environ.get('Z_TOOL_API', 'https://host.docker.internal:5003')
ADMIN_URL = os.environ.get('ADMIN_URL', 'https://host.docker.internal:44003')
LEARNER_URL = os.environ.get('LEARNER_URL', 'https://host.docker.internal:44010')
AUTHOR_URL = os.environ.get('AUTHOR_URL', 'https://host.docker.internal:44020')
AUTHOR_REACT_URL = os.environ.get('AUTHOR_URL', 'https://host.docker.internal:44017')
IDENTITY_SERVER = os.environ.get('IDENTITY_SERVER', 'https://host.docker.internal:5001')
IDENTITY_API = os.environ.get('IDENTITY_API', 'https://host.docker.internal:5011')

MINIO_FOLDER = 'autotests'
MINIO_HOST = os.environ.get('MINIO_HOST', 'host.docker.internal:9000')
MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY', 'minio_access_key')
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY', 'minio_secret_key')
MINIO_PRIVATE_BUCKET_NAME = os.environ.get('MINIO_PRIVATE_BUCKET_NAME', 'minio-private-bucket-name')
MINIO_PUBLIC_BUCKET_NAME = os.environ.get('MINIO_PUBLIC_BUCKET_NAME', 'minio-public-bucket-name')

REQUESTS_LOGGING = False

models_manager.settings.DATABASE = {
    'host': os.environ.get('DB_HOST', 'host.docker.internal'),
    'port': os.environ.get('DB_POST', 5432),
    'user': os.environ.get('DB_USER', 'alms'),
    'password': os.environ.get('DB_PASSWORD', 'alms'),
}
IDENTITY_DB_NAME = os.environ.get('IDENTITY_DB_NAME', 'identity')
USERS_DB_NAME = os.environ.get('USERS_DB_NAME', 'users')
ZTOOL_DB_NAME = os.environ.get('ZTOOL_DB_NAME', 'ztool')
models_manager.settings.DATABASES = [IDENTITY_DB_NAME, USERS_DB_NAME, ZTOOL_DB_NAME]

models_manager.settings.DATABASE_LOGGING = True

DEFAULT_USER = {
    "id": "aa447a3e-84dd-4aa1-9b78-84fa21e6191c",
    "username": "zara@company.com",
    "password": "Pass123$",
    "client_id": "insomnia",
    "client_secret": "insomnia",
    "grant_type": "password",
    "first_name": "Zara",
    "last_name": "Bond"
}

LAB_APPLICATION_USER = {
    "user": "labs",
    "password": "dqw4w9wgxcq"
}

DEFAULT_TENANT = {
    "id": "39e7fbd8-c4f3-456a-a744-dd43862ba8d3",
    "name": "Autotest"
}

LANGUAGE = os.environ.get('LANGUAGE', 'en-US')

GITLAB = os.environ.get('CI_PROJECT_URL')

SLACK_CHANNEL = 'dev-alms-gitlab'
SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN')

ALLURE_ENDPOINT = os.environ.get('ALLURE_ENDPOINT')
ALLURE_PROJECT_ID = os.environ.get('ALLURE_PROJECT_ID')
ALLURE_USERNAME = os.environ.get('ALLURE_USERNAME')
ALLURE_PASSWORD = os.environ.get('ALLURE_PASSWORD')

api_manager.settings.PROJECT = Project.ALMS
api_manager.settings.ALMS_IDENTITY_SERVER = IDENTITY_SERVER
api_manager.settings.ALMS_USER = DEFAULT_USER
api_manager.settings.CERT_PATH = CERT_PATH
api_manager.settings.ALMS_USERS_API = USERS_API
api_manager.settings.WAIT_TIMEOUT = WAIT_TIMEOUT

alms_integration.settings.ALMS_USER = DEFAULT_USER
alms_integration.settings.ALMS_TENANT = DEFAULT_TENANT
alms_integration.settings.ALMS_USERS_API = f'{USERS_API}/api/v1'
