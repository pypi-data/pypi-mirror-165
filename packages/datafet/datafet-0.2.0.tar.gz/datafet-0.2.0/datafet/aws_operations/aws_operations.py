import base64
import logging
from typing import Optional

import ecdsa
from ecdsa import SigningKey, VerifyingKey
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import (
    DeleteObjectOutputTypeDef,
    GetObjectOutputTypeDef,
    PutObjectOutputTypeDef,
)
from mypy_boto3_secretsmanager import SecretsManagerClient
from mypy_boto3_secretsmanager.type_defs import GetSecretValueResponseTypeDef
from mypy_boto3_sqs import SQSClient
from mypy_boto3_sqs.type_defs import SendMessageResultTypeDef

LOG = logging.getLogger(__name__)


#
# SecretsManager
#


def get_secret_string(
    secrets_manager_client: SecretsManagerClient, secret_id: str
) -> Optional[str]:
    try:
        secret_response: GetSecretValueResponseTypeDef = (
            secrets_manager_client.get_secret_value(SecretId=secret_id)
        )
        secret_string_maybe = secret_response.get("SecretString", None)
        if secret_string_maybe:
            return secret_string_maybe
        else:
            LOG.error(
                f"""
                    Could not read secret {secret_id} becasue
                    GetSecretValueResponse does not have a SecretString field.
                    The secret might be binary instead of string.
                """
            )
            return None
    except Exception as ex:
        LOG.error(f"Could not read secret {secret_id} becasue of {ex}")
        return None


def get_secret_binary(
    secrets_manager_client: SecretsManagerClient, secret_id: str
) -> Optional[bytes]:
    try:
        secret_response: GetSecretValueResponseTypeDef = (
            secrets_manager_client.get_secret_value(SecretId=secret_id)
        )
        secret_bytes_maybe = secret_response.get("SecretBinary", None)
        if secret_bytes_maybe:
            return secret_bytes_maybe
        else:
            LOG.error(
                f"""
                    Could not read secret {secret_id} becasue
                    GetSecretValueResponse does not have a SecretBinary field.
                    The secret might be string instead of bytes.
                """
            )
            return None
    except Exception as ex:
        LOG.error(f"Could not read secret {secret_id} becasue of {ex}")
        return None


def get_signing_key(
    secrets_manager_client: SecretsManagerClient, secret_id: str
) -> Optional[SigningKey]:
    try:
        signing_key_b64 = get_secret_binary(
            secrets_manager_client=secrets_manager_client, secret_id=secret_id
        )
        if signing_key_b64:
            signing_key_der = base64.b64decode(signing_key_b64)
            return ecdsa.SigningKey.generate().from_der(signing_key_der)
        else:
            return None
    except Exception as ex:
        LOG.error(f"Could not get signing key because of {ex}")
        return None


def get_verifying_key(
    secrets_manager_client: SecretsManagerClient, secret_id: str
) -> Optional[VerifyingKey]:
    try:
        signing_key = get_signing_key(
            secrets_manager_client=secrets_manager_client, secret_id=secret_id
        )
        if signing_key:
            return signing_key.get_verifying_key()
        else:
            return None
    except Exception as ex:
        LOG.error(f"Could not get verifying key because of {ex}")
        return None


#
# S3
#


def get_s3_object(
    s3_client: S3Client, bucket: str, key: str
) -> Optional[GetObjectOutputTypeDef]:
    try:
        return s3_client.get_object(Bucket=bucket, Key=key)
    except Exception as ex:
        LOG.error(f"Could not read object bucket: {bucket} key: {key} becasue of {ex}")
        return None


def delete_s3_object(
    s3_client: S3Client, bucket: str, key: str
) -> Optional[DeleteObjectOutputTypeDef]:
    try:
        return s3_client.delete_object(Bucket=bucket, Key=key)
    except Exception as ex:
        LOG.error(
            f"Could not delete object bucket: {bucket} key: {key} becasue of {ex}"
        )
        return None


#
# S3
#


def save_to_s3(
    s3_client: S3Client,
    bucket: str,
    key: str,
    body: str,
) -> Optional[PutObjectOutputTypeDef]:
    try:
        return s3_client.put_object(Bucket=bucket, Key=key, Body=body)
    except Exception as ex:
        LOG.error(f"Could not put object bucket: {bucket} key: {key} becasue of {ex}")
        return None


#
# SQS
#


def send_sqs_message(
    sqs_client: SQSClient, queue_url: str, message_body: str
) -> Optional[SendMessageResultTypeDef]:
    try:
        return sqs_client.send_message(QueueUrl=queue_url, MessageBody=message_body)
    except Exception as ex:
        LOG.error(
            f"Could not send SQS message {message_body} to queue_url: {queue_url} becasue of {ex}"
        )
        return None


def send_sqs_message_fifo(
    sqs_client: SQSClient, queue_url: str, message_body: str, message_group_id: str
):
    try:
        return sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageGroupId=message_group_id,
        )
    except Exception as ex:
        LOG.error(
            f"""Could not send SQS message {message_body}
                to queue_url: {queue_url}
                message_group_id: {message_group_id} becasue of {ex}
            """
        )
        return None
