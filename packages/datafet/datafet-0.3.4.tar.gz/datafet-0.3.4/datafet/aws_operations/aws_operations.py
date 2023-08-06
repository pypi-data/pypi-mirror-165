import logging
from typing import Union

from botocore.response import StreamingBody
from datafet.http_return import http_404_json, http_500_json, json_error
from fastapi.responses import JSONResponse
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import GetObjectOutputTypeDef, PutObjectOutputTypeDef
from mypy_boto3_secretsmanager import SecretsManagerClient
from mypy_boto3_secretsmanager.type_defs import GetSecretValueResponseTypeDef
from mypy_boto3_sqs import SQSClient
from mypy_boto3_sqs.type_defs import SendMessageResultTypeDef

LOG = logging.getLogger(__name__)


#
# SecretsManager
#


e = [
    "ClientError",
    "DecryptionFailure",
    "EncryptionFailure",
    "InternalServiceError",
    "InvalidNextTokenException",
    "InvalidParameterException",
    "InvalidRequestException",
    "LimitExceededException",
    "MalformedPolicyDocumentException",
    "PreconditionNotMetException",
    "PublicPolicyException",
    "ResourceExistsException",
    "ResourceNotFoundException",
]


def get_secret_string(
    secrets_manager_client: SecretsManagerClient, secret_id: str
) -> Union[str, JSONResponse]:
    try:
        secret_response: GetSecretValueResponseTypeDef = (
            secrets_manager_client.get_secret_value(SecretId=secret_id)
        )
        secret_string_maybe = secret_response.get("SecretString", None)
        if secret_string_maybe:
            return secret_string_maybe
        else:
            return http_404_json(
                "SecretsManager Error",
                [
                    (
                        f"Could not get secret {secret_id} becasue GetSecretValueResponse does not have a SecretString field."
                        f"The secret might be binary instead of string."
                    )
                ],
            )

    except secrets_manager_client.exceptions.ClientError as ce:
        status_code = ce.response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500)
        error_code = ce.response.get("Error", {}).get("Code", "ErrorCodeMissing")
        return json_error(
            status_code=status_code,
            message="SecretsManager Error",
            reasons=[
                f"Could not get {secret_id} and a ClientError happened with status code: {status_code}",
                error_code,
            ],
        )

    except Exception as ex:
        return json_error(
            status_code=500,
            message="SecretsManager Error",
            reasons=[f"Could not get {secret_id} and an exception happened: {ex}"],
        )


def get_secret_binary(
    secrets_manager_client: SecretsManagerClient, secret_id: str
) -> Union[bytes, JSONResponse]:
    try:
        secret_response: GetSecretValueResponseTypeDef = (
            secrets_manager_client.get_secret_value(SecretId=secret_id)
        )
        secret_bytes_maybe = secret_response.get("SecretBinary", None)
        if secret_bytes_maybe:
            return secret_bytes_maybe
        else:
            return http_404_json(
                "SecretsManager Error",
                [
                    (
                        f"Could not get secret {secret_id} becasue GetSecretValueResponse does not have a SecretString field."
                        f"The secret might be string instead of binary."
                    )
                ],
            )

    except secrets_manager_client.exceptions.ClientError as ce:
        status_code = ce.response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500)
        error_code = ce.response.get("Error", {}).get("Code", "ErrorCodeMissing")
        return json_error(
            status_code=status_code,
            message="SecretsManager Error",
            reasons=[
                f"Could not get {secret_id} and a ClientError happened with status code: {status_code}",
                error_code,
            ],
        )

    except Exception as ex:
        return json_error(
            status_code=500,
            message="SecretsManager Error",
            reasons=[f"Could not get {secret_id} and an exception happened: {ex}"],
        )


#
# S3
#


e = [
    "BucketAlreadyExists",
    "BucketAlreadyOwnedByYou",
    "ClientError",
    "InvalidObjectState",
    "NoSuchBucket",
    "NoSuchKey",
    "NoSuchUpload",
    "ObjectAlreadyInActiveTierError",
    "ObjectNotInActiveTierError",
]


def s3_get_object_stream(
    s3_client: S3Client, s3_bucket: str, s3_key: str
) -> Union[StreamingBody, JSONResponse]:
    try:
        s3_response: GetObjectOutputTypeDef = s3_client.get_object(
            Bucket=s3_bucket, Key=s3_key
        )
        s3_stream_maybe = s3_response.get("Body")

        if s3_stream_maybe is None:
            return http_500_json(
                "S3 Error", [f"Could not get Body field from s3 response"]
            )

        s3_stream_maybe.set_socket_timeout(3)
        return s3_stream_maybe

    except (s3_client.exceptions.NoSuchKey, s3_client.exceptions.NoSuchBucket) as ce:
        error_code = ce.response.get("Error", {}).get("Code", "ErrorCodeMissing")
        return http_404_json(
            "S3 Error", [f"Could not get s3://{s3_bucket}/{s3_key}", error_code]
        )

    except s3_client.exceptions.ClientError as ce:
        status_code = ce.response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500)
        error_code = ce.response.get("Error", {}).get("Code", "ErrorCodeMissing")
        return json_error(
            status_code=status_code,
            message="S3 Error",
            reasons=[
                f"Could not get s3://{s3_bucket}/{s3_key} and a ClientError happened with status code: {status_code}",
                error_code,
            ],
        )

    except Exception as ex:
        LOG.error(f"Error: S3 Error. Reasons: {ex}")
        return json_error(
            status_code=500,
            message="S3 Error",
            reasons=[
                f"Could not get s3://{s3_bucket}/{s3_key} and a Exception happened: {ex}"
            ],
        )


def s3_get_object_bytes(
    s3_client: S3Client, s3_bucket: str, s3_key: str
) -> Union[bytes, JSONResponse]:
    try:

        s3_stream_maybe = s3_get_object_stream(
            s3_client=s3_client, s3_bucket=s3_bucket, s3_key=s3_key
        )

        if isinstance(s3_stream_maybe, StreamingBody):
            return s3_stream_maybe.read()
        else:
            return s3_stream_maybe

    except Exception as ex:
        LOG.error(f"Error: Unexpected error. Reasons: {ex}")
        return json_error(
            status_code=500,
            message="S3 Error",
            reasons=[
                f"Could not get key s3://{s3_bucket}/{s3_key} and a Exception happened: {ex}"
            ],
        )


def s3_put_object_bytes(
    s3_client: S3Client, s3_bucket: str, s3_key: str, s3_body_bytes: bytes
) -> Union[PutObjectOutputTypeDef, JSONResponse]:
    try:
        s3_response: PutObjectOutputTypeDef = s3_client.put_object(
            Bucket=s3_bucket, Key=s3_key, Body=s3_body_bytes
        )

        return s3_response

    except s3_client.exceptions.NoSuchBucket:
        return http_404_json("S3 Error", [f"Could not find bucket: {s3_bucket}"])

    except s3_client.exceptions.ClientError as ce:
        status_code = ce.response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500)
        error_code = ce.response.get("Error", {}).get("Code", "ErrorCodeMissing")
        return json_error(
            status_code=status_code,
            message="S3 Error",
            reasons=[
                f"Could not put key s3://{s3_bucket}/{s3_key} and a ClientError happened with status code: {status_code}",
                error_code,
            ],
        )

    except Exception as ex:
        return json_error(
            status_code=500,
            message="S3 Error",
            reasons=[
                f"Could not put key s3://{s3_bucket}/{s3_key} and a Exception happened: {ex}"
            ],
        )


e = [
    "BatchEntryIdsNotDistinct",
    "BatchRequestTooLong",
    "ClientError",
    "EmptyBatchRequest",
    "InvalidAttributeName",
    "InvalidBatchEntryId",
    "InvalidIdFormat",
    "InvalidMessageContents",
    "MessageNotInflight",
    "OverLimit",
    "PurgeQueueInProgress",
    "QueueDeletedRecently",
    "QueueDoesNotExist",
    "QueueNameExists",
    "ReceiptHandleIsInvalid",
    "TooManyEntriesInBatchRequest",
    "UnsupportedOperation",
]


def send_sqs_message_fifo(
    sqs_client: SQSClient, queue_url: str, message_body: str, message_group_id: str
) -> Union[SendMessageResultTypeDef, JSONResponse]:
    try:
        return sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageGroupId=message_group_id,
        )
    except sqs_client.exceptions.ClientError as ce:
        status_code = ce.response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500)
        error_code = ce.response.get("Error", {}).get("Code", "ErrorCodeMissing")
        return json_error(
            status_code,
            "SQS Error",
            [f"Could not send message to queue: {queue_url}", error_code],
        )
    except Exception as ex:
        message, reasons = "SQS Error", [
            (
                f"Could not send SQS message {message_body} to queue_url: {queue_url}"
                f"message_group_id: {message_group_id} becasue of {ex}"
            )
        ]
        return http_500_json(message=message, reasons=reasons)


# import boto3

# sqs = boto3.client("sqs")
# [e for e in dir(sqs.exceptions) if e[0].isupper()]

# s3 = boto3.client("s3")
# [e for e in dir(s3.exceptions) if e[0].isupper()]
