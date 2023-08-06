from enum import Enum
from typing import List

from pydantic import BaseModel, EmailStr

#
# GENERIC
#


class CustomError(BaseModel):
    message: str
    reasons: List[str]


#
# HTTP
#


class HttpSuccess(BaseModel):
    ok: str


class HttpError(BaseModel):
    status_code: int
    error: CustomError


#
# JWT
#


class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"


class JwtParam(BaseModel):
    email: EmailStr
    first_name: str
    role: RoleEnum
