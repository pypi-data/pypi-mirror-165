from typing import Any, Dict, Optional, Union

from datafet.http_return import http_400_json as http_400_json
from datafet.http_return import json_error as json_error
from ecdsa import SigningKey as SigningKey
from ecdsa import VerifyingKey as VerifyingKey
from fastapi.responses import JSONResponse as JSONResponse
from pydantic import BaseModel
from pydantic import EmailStr as EmailStr

DEFAULT_ALGORITHM: str

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
    algorithm=...,
) -> Optional[str]: ...
def decode_jwt(
    jwt_string: str, verifying_key: VerifyingKey, audience: str, algorithm=...
) -> Optional[Dict[str, Any]]: ...
def get_jwt_field(
    cookies: Dict[str, str], verifying_key: VerifyingKey, audience: str, field: str
) -> Union[str, JSONResponse]: ...
def get_user_email(
    cookies: Dict[str, str], verifying_key: VerifyingKey, audience: str
) -> Union[str, JSONResponse]: ...
def get_user_role(
    cookies: Dict[str, str], verifying_key: VerifyingKey, audience: str
) -> Union[str, JSONResponse]: ...
