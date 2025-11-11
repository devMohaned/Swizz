from datetime import datetime, UTC

from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from service.dto.error_response import ErrorModel
from .app_exceptions import AppException
from .error_code import INTERNAL_SERVER_ERROR, BAD_REQUEST
from core.logging import get_logger
logger = get_logger(__name__)

async def app_exception_handler(request: Request, exc: AppException):
    request_id = getattr(request.state, "request_id", None)
    payload = ErrorModel(
        message=exc.detail["message"],
        code=exc.detail["code"],
        status=exc.status_code,
        requestId=request_id,
        timestamp=datetime.now(UTC),
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump(mode="json"))


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = getattr(request.state, "request_id", None)
    payload = ErrorModel(
        message=f"Invalid request data.",
        code=BAD_REQUEST,
        status=status.HTTP_400_BAD_REQUEST,
        requestId=request_id,
        timestamp=datetime.now(UTC),
    )
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=payload.model_dump(mode="json"))


async def general_http_exception_handler(request: Request, exc: HTTPException):
    request_id = getattr(request.state, "request_id", None)
    payload = ErrorModel(
        message=f"An unexpected HTTP error occurred. Reason {exc}",
        code=INTERNAL_SERVER_ERROR,
        status=exc.status_code,
        requestId=request_id,
        timestamp=datetime.now(UTC),
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump(mode="json"))


async def general_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)
    payload = ErrorModel(
        message=f"An unexpected error occurred.",
        code=INTERNAL_SERVER_ERROR,
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        requestId=request_id,
        timestamp=datetime.now(UTC),
    )
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=payload.model_dump(mode="json"))
