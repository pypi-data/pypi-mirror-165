from typing import Union

from _typeshed import Incomplete
from botocore.response import StreamingBody
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import PutObjectOutputTypeDef
from mypy_boto3_secretsmanager import SecretsManagerClient
from mypy_boto3_sqs import SQSClient
from mypy_boto3_sqs.type_defs import SendMessageResultTypeDef

from ..custom_types import HttpError as HttpError
from ..http_return import http_error as http_error

e: Incomplete

def get_secret_string(
    secrets_manager_client: SecretsManagerClient, secret_id: str
) -> Union[str, HttpError]: ...
def get_secret_binary(
    secrets_manager_client: SecretsManagerClient, secret_id: str
) -> Union[bytes, HttpError]: ...
def s3_get_object_stream(
    s3_client: S3Client, s3_bucket: str, s3_key: str
) -> Union[StreamingBody, HttpError]: ...
def s3_get_object_bytes(
    s3_client: S3Client, s3_bucket: str, s3_key: str
) -> Union[bytes, HttpError]: ...
def s3_put_object_bytes(
    s3_client: S3Client, s3_bucket: str, s3_key: str, s3_body_bytes: bytes
) -> Union[PutObjectOutputTypeDef, HttpError]: ...
def send_sqs_message_fifo(
    sqs_client: SQSClient, queue_url: str, message_body: str, message_group_id: str
) -> Union[SendMessageResultTypeDef, HttpError]: ...
