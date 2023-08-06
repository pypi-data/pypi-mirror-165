import base64
from typing import Union

import ecdsa
from datafet.aws_operations import (
    get_secret_binary,
    s3_put_object_bytes,
    send_sqs_message_fifo,
)
from datafet.http_return.http_return import json_error
from ecdsa import SigningKey
from fastapi.responses import JSONResponse
from mypy_boto3_s3 import S3Client
from mypy_boto3_secretsmanager import SecretsManagerClient
from mypy_boto3_sqs import SQSClient


def save_to_s3_and_send_sqs_update(
    s3_client: S3Client,
    s3_bucket: str,
    s3_key: str,
    s3_body_bytes: bytes,
    sqs_client: SQSClient,
    sqs_queue_url: str,
    sqs_message_body: str,
    sqs_message_group_id: str,
) -> Union[bool, JSONResponse]:

    s3_response = s3_put_object_bytes(
        s3_client=s3_client,
        s3_bucket=s3_bucket,
        s3_key=s3_key,
        s3_body_bytes=s3_body_bytes,
    )

    if isinstance(s3_response, JSONResponse):
        return s3_response

    sqs_message_sent = send_sqs_message_fifo(
        sqs_client=sqs_client,
        queue_url=sqs_queue_url,
        message_body=sqs_message_body,
        message_group_id=sqs_message_group_id,
    )

    if isinstance(sqs_message_sent, JSONResponse):
        return sqs_message_sent

    return True


def get_signing_key(
    secrets_manager_client: SecretsManagerClient, secret_id: str
) -> Union[SigningKey, JSONResponse]:
    try:
        signing_key_b64_maybe = get_secret_binary(
            secrets_manager_client=secrets_manager_client, secret_id=secret_id
        )
        if isinstance(signing_key_b64_maybe, JSONResponse):
            return signing_key_b64_maybe

        signing_key_der = base64.b64decode(signing_key_b64_maybe)
        return ecdsa.SigningKey.generate().from_der(signing_key_der)
    except Exception as ex:
        return json_error(
            status_code=500,
            message="SigningKey Error",
            reasons=[
                f"Could not fetch signing key: {secret_id} and a Exception happened: {ex}"
            ],
        )
