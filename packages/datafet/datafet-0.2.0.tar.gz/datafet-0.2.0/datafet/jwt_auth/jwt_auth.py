import logging
import time
from typing import Any, Dict, Optional

import jwt
from ecdsa import SigningKey, VerifyingKey
from pydantic import BaseModel, EmailStr

LOG = logging.getLogger(__name__)


DEFAULT_ALGORITHM = "ES256"


class JwtParam(BaseModel):
    email: EmailStr
    firstName: str
    domain: str


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
                "email": jwt_param.email,
                "firstName": jwt_param.firstName,
                "domain": jwt_param.domain,
                "aud": audience,
                "exp": expiry,
                "iss": issuer,
                "iat": now,
                "nbf": now,
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


def is_valid_jwt(
    jwt_string: str,
    verifying_key: VerifyingKey,
    audience: str,
    algorithm=DEFAULT_ALGORITHM,
):
    try:
        decoded = decode_jwt(jwt_string, verifying_key, audience, algorithm)
        if decoded:
            return True
    except Exception as _ex:
        return False
