from typing import Any, List

from fastapi.responses import JSONResponse
from pydantic import BaseModel

class HttpSuccess(BaseModel):
    ok: str

class CustomJsonError(BaseModel):
    message: str
    reasons: List[str]

class HttpError(BaseModel):
    statusCode: int
    error: CustomJsonError

def process_pydantic_validation(v): ...
def json_response(status_code: int, content: Any) -> JSONResponse: ...
def json_error(status_code: int, message: str, reasons: List[str]) -> JSONResponse: ...
def http_200_json(jsonable_content) -> JSONResponse: ...
def http_400_json(message: str, reasons: List[str]) -> JSONResponse: ...
def http_403_json(message: str, reasons: List[str]) -> JSONResponse: ...
def http_404_json(message: str, reasons: List[str]) -> JSONResponse: ...
def http_500_json(message: str, reasons: List[str]) -> JSONResponse: ...
def json_http_200_with_cookie(
    content,
    key: str,
    value: str,
    max_age: int,
    secure: bool,
    httponly: bool,
    domain: str,
) -> JSONResponse: ...
