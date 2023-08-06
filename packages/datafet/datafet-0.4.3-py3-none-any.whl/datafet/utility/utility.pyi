from typing import Dict, Union

from ecdsa import SigningKey as SigningKey
from ecdsa import VerifyingKey as VerifyingKey
from mypy_boto3_s3 import S3Client
from mypy_boto3_secretsmanager import SecretsManagerClient
from mypy_boto3_sqs import SQSClient

from ..aws_operations import get_secret_binary as get_secret_binary
from ..aws_operations import s3_put_object_bytes as s3_put_object_bytes
from ..aws_operations import send_sqs_message_fifo as send_sqs_message_fifo
from ..custom_types import CustomError as CustomError
from ..custom_types import HttpError as HttpError
from ..http_return import http_error as http_error
from ..jwt_auth import decode_jwt as decode_jwt

def save_to_s3_and_send_sqs_update(
    s3_client: S3Client,
    s3_bucket: str,
    s3_key: str,
    s3_body_bytes: bytes,
    sqs_client: SQSClient,
    sqs_queue_url: str,
    sqs_message_body: str,
    sqs_message_group_id: str,
) -> Union[bool, HttpError]: ...
def get_signing_key(
    secrets_manager_client: SecretsManagerClient, secret_id: str
) -> Union[SigningKey, HttpError]: ...
def get_jwt_token_from_cookies(
    cookies: Dict[str, str], name_of_jwt: str
) -> Union[str, CustomError]: ...
def get_jwt_field_from_cookies(
    cookies: Dict[str, str],
    name_of_jwt: str,
    verifying_key: VerifyingKey,
    audience: str,
    jwt_field_name: str,
) -> Union[str, CustomError]: ...
def get_user_email_from_cookies(
    cookies: Dict[str, str],
    name_of_jwt: str,
    verifying_key: VerifyingKey,
    audience: str,
) -> Union[str, CustomError]: ...
def get_user_role_from_cookies(
    cookies: Dict[str, str],
    name_of_jwt: str,
    verifying_key: VerifyingKey,
    audience: str,
) -> Union[str, CustomError]: ...
