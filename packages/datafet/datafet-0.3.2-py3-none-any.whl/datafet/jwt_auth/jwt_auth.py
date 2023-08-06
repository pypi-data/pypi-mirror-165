import logging
import time
from typing import Any, Dict, Optional, Union

import jwt
from datafet.http_return import http_400_json, json_error
from ecdsa import SigningKey, VerifyingKey
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

LOG = logging.getLogger(__name__)


DEFAULT_ALGORITHM = "ES256"


class JwtParam(BaseModel):
    email: EmailStr
    first_name: str
    role: str


def create_jwt(
    jwt_param: JwtParam,
    signing_key: SigningKey,
    audience: str,
    issuer: str,
    exp_days: int,
    algorithm=DEFAULT_ALGORITHM,
) -> Optional[str]:
    try:
        now = int(time.time())
        expiry = now + exp_days * 24 * 60 * 60
        return jwt.encode(
            {
                "aud": audience,
                "email": jwt_param.email,
                "exp": expiry,
                "first_name": jwt_param.first_name,
                "iat": now,
                "iss": issuer,
                "nbf": now,
                "role": jwt_param.role,
            },
            signing_key.to_pem(),
            algorithm=algorithm,
        )
    except Exception as ex:
        LOG.error(f"{ex}")
        return None


def decode_jwt(
    jwt_string: str,
    verifying_key: VerifyingKey,
    audience: str,
    algorithm=DEFAULT_ALGORITHM,
) -> Optional[Dict[str, Any]]:

    try:
        return jwt.decode(
            jwt=jwt_string,
            key=verifying_key.to_pem(),
            algorithms=[algorithm],
            audience=audience,
        )
    except Exception as ex:
        LOG.error(f"{ex}")
        return None


def get_jwt_field(
    cookies: Dict[str, str], verifying_key: VerifyingKey, audience: str, field: str
) -> Union[str, JSONResponse]:

    try:

        jwt_string = cookies.get("jwt", None)
        if jwt_string is None:
            return http_400_json("JWT Error", [f"Could not find JWT in cookies."])

        decoded_jwt = decode_jwt(
            jwt_string=jwt_string,
            verifying_key=verifying_key,
            audience=audience,
        )
        if decoded_jwt is None:
            return http_400_json(
                message="JWT Error",
                reasons=["Could not decode JWT."],
            )

        user_email_maybe = decoded_jwt.get(field, None)

        if user_email_maybe is None:
            return http_400_json(
                message="JWT Error",
                reasons=["Could not decode JWT. Email might be missing."],
            )

        return str(user_email_maybe)

    except Exception as ex:
        LOG.error(
            f"Error: JWT Error. Reasons: Could not get user email from JWT token and a Exception happened: {ex}"
        )
        return json_error(
            status_code=500,
            message="JWT Error",
            reasons=[
                f"Could not get user email from JWT token and a Exception happened: {ex}"
            ],
        )


def get_user_email(
    cookies: Dict[str, str], verifying_key: VerifyingKey, audience: str
) -> Union[str, JSONResponse]:

    return get_jwt_field(cookies, verifying_key, audience, "email")


def get_user_role(
    cookies: Dict[str, str], verifying_key: VerifyingKey, audience: str
) -> Union[str, JSONResponse]:

    return get_jwt_field(cookies, verifying_key, audience, "role")
