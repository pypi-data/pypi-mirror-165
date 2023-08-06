import base64
from typing import Any, Dict, Union

import ecdsa
from ecdsa import SigningKey, VerifyingKey
from mypy_boto3_s3 import S3Client
from mypy_boto3_secretsmanager import SecretsManagerClient
from mypy_boto3_sqs import SQSClient

from ..aws_operations import (
    get_secret_binary,
    s3_put_object_bytes,
    send_sqs_message_fifo,
)
from ..custom_types import CustomError, HttpError
from ..http_return import http_error
from ..jwt_auth import decode_jwt


def save_to_s3_and_send_sqs_update(
    s3_client: S3Client,
    s3_bucket: str,
    s3_key: str,
    s3_body_bytes: bytes,
    sqs_client: SQSClient,
    sqs_queue_url: str,
    sqs_message_body: str,
    sqs_message_group_id: str,
) -> Union[bool, HttpError]:

    s3_response = s3_put_object_bytes(
        s3_client=s3_client,
        s3_bucket=s3_bucket,
        s3_key=s3_key,
        s3_body_bytes=s3_body_bytes,
    )
    if isinstance(s3_response, HttpError):
        return s3_response

    sqs_message_sent = send_sqs_message_fifo(
        sqs_client=sqs_client,
        queue_url=sqs_queue_url,
        message_body=sqs_message_body,
        message_group_id=sqs_message_group_id,
    )
    if isinstance(sqs_message_sent, HttpError):
        return sqs_message_sent

    return True


def get_signing_key(
    secrets_manager_client: SecretsManagerClient, secret_id: str
) -> Union[SigningKey, HttpError]:
    try:
        signing_key_b64_maybe = get_secret_binary(
            secrets_manager_client=secrets_manager_client, secret_id=secret_id
        )
        if isinstance(signing_key_b64_maybe, HttpError):
            return signing_key_b64_maybe

        signing_key_der = base64.b64decode(signing_key_b64_maybe)
        return ecdsa.SigningKey.generate().from_der(signing_key_der)
    except Exception as ex:
        return http_error(
            status_code=500,
            message="SigningKey Error",
            reasons=[
                f"Could not fetch signing key: {secret_id} and a Exception happened: {ex}"
            ],
        )


def get_jwt_token_from_cookies(
    cookies: Dict[str, Any], name_of_jwt: str
) -> Union[str, CustomError]:
    return cookies.get(
        name_of_jwt,
        CustomError(message="Cookie Error", reasons=["Could not get JWT from cookies"]),
    )


def get_jwt_field_from_cookies(
    cookies: Dict[str, Any],
    name_of_jwt: str,
    verifying_key: VerifyingKey,
    audience: str,
    jwt_field_name: str,
) -> Union[str, CustomError]:
    try:
        jwt_token_maybe = get_jwt_token_from_cookies(cookies, name_of_jwt)
        if isinstance(jwt_token_maybe, CustomError):
            return jwt_token_maybe

        jwt_decoded_maybe = decode_jwt(jwt_token_maybe, verifying_key, audience)
        if isinstance(jwt_decoded_maybe, CustomError):
            return jwt_decoded_maybe

        return jwt_decoded_maybe.get(
            jwt_field_name,
            CustomError(
                message="JWT Error", reasons=["Could not get field from JWT token"]
            ),
        )
    except Exception as ex:
        return CustomError(
            message="JWT Error", reasons=[f"Could not get field from JWT token {ex}"]
        )


def get_user_email_from_cookies(
    cookies: Dict[str, Any],
    name_of_jwt: str,
    verifying_key: VerifyingKey,
    audience: str,
) -> Union[str, CustomError]:
    return get_jwt_field_from_cookies(
        cookies, name_of_jwt, verifying_key, audience, "email"
    )


def get_user_role_from_cookies(
    cookies: Dict[str, Any],
    name_of_jwt: str,
    verifying_key: VerifyingKey,
    audience: str,
) -> Union[str, CustomError]:
    return get_jwt_field_from_cookies(
        cookies, name_of_jwt, verifying_key, audience, "role"
    )
