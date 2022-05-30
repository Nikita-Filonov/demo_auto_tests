"""S3 file storage client"""

import urllib3
from minio import Minio

from settings import CERT_PATH, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_HOST

http_client = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=CERT_PATH
)

storage_client = Minio(
    MINIO_HOST,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    http_client=http_client
)
