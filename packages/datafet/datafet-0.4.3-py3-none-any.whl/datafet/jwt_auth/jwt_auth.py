import time
from typing import Any, Dict, Union

import jwt
from ecdsa import SigningKey, VerifyingKey

from ..custom_types import CustomError, JwtParam

DEFAULT_ALGORITHM = "ES256"


def create_jwt(
    jwt_param: JwtParam,
    signing_key: SigningKey,
    audience: str,
    issuer: str,
    exp_days: int,
    algorithm=DEFAULT_ALGORITHM,
) -> Union[str, CustomError]:
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
        return CustomError(message="JWT Encoding Error", reasons=[f"{ex}"])


def decode_jwt(
    jwt_string: str,
    verifying_key: VerifyingKey,
    audience: str,
    algorithm=DEFAULT_ALGORITHM,
) -> Union[Dict[str, Any], CustomError]:
    try:
        return jwt.decode(
            jwt=jwt_string,
            key=verifying_key.to_pem(),
            algorithms=[algorithm],
            audience=audience,
        )
    except Exception as ex:
        return CustomError(message="JWT Decoding Error", reasons=[f"{ex}"])
