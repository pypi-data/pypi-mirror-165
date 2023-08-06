from enum import Enum
from typing import List

from pydantic import BaseModel
from pydantic import EmailStr as EmailStr

class CustomError(BaseModel):
    message: str
    reasons: List[str]

class HttpSuccess(BaseModel):
    ok: str

class HttpError(BaseModel):
    status_code: int
    error: CustomError

class RoleEnum(str, Enum):
    user: str
    admin: str

class JwtParam(BaseModel):
    email: EmailStr
    first_name: str
    role: RoleEnum
