from typing import Any, List

from datafet.custom_types import CustomError
from datafet.custom_types.custom_types import HttpError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#
# PYDANTIC ERROR
#


def process_pydantic_validation(v):
    def get_loc(d):
        return d.get("loc", (None,))[1]

    def get_type(d):
        return d.get("type", ".").split(".")[1]

    return list(map(lambda x: f"{get_loc(x)}:{get_type(x)}", v))


#
# Generic
#


def json_response(status_code: int, content: Any) -> JSONResponse:
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))


def json_error(status_code: int, message: str, reasons: List[str]) -> JSONResponse:
    return json_response(status_code, CustomError(message=message, reasons=reasons))


def http_error(status_code: int, message: str, reasons: List[str]) -> HttpError:
    return HttpError(status_code, CustomError(message, reasons))


#
# 2xx
#


def http_200_json(jsonable_content) -> JSONResponse:
    return json_response(200, jsonable_content)


#
# 4xx
#


def http_400_json(message: str, reasons: List[str]) -> JSONResponse:
    return json_response(400, CustomError(message=message, reasons=reasons))


def http_403_json(message: str, reasons: List[str]) -> JSONResponse:
    return json_response(403, CustomError(message=message, reasons=reasons))


def http_404_json(message: str, reasons: List[str]) -> JSONResponse:
    return json_response(404, CustomError(message=message, reasons=reasons))


#
# 5xx
#


def http_500_json(message: str, reasons: List[str]) -> JSONResponse:
    return json_response(500, CustomError(message=message, reasons=reasons))


def http_200_json_with_cookie(
    content,
    key: str,
    value: str,
    max_age: int,
    secure: bool,
    httponly: bool,
    domain: str,
) -> JSONResponse:
    response = http_200_json(content)
    response.set_cookie(
        key=key,
        value=value,
        max_age=max_age,
        secure=secure,
        httponly=httponly,
        domain=domain,
    )
    return response
