from typing import Any, Dict, Union

from datafet.custom_types import CustomError as CustomError
from datafet.custom_types import JwtParam as JwtParam
from ecdsa import SigningKey as SigningKey
from ecdsa import VerifyingKey as VerifyingKey

DEFAULT_ALGORITHM: str

def create_jwt(
    jwt_param: JwtParam,
    signing_key: SigningKey,
    audience: str,
    issuer: str,
    exp_days: int,
    algorithm=...,
) -> Union[str, CustomError]: ...
def decode_jwt(
    jwt_string: str, verifying_key: VerifyingKey, audience: str, algorithm=...
) -> Union[Dict[str, Any], CustomError]: ...
