from datetime import datetime, UTC

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from .error_code import INTERNAL_SERVER_ERROR
from service.dto.error_response import ErrorModel


async def general_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)
    payload = ErrorModel(
        message="An unexpected error occurred.",
        code=INTERNAL_SERVER_ERROR,
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        requestId=request_id,
        timestamp=datetime.now(UTC),
    )
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=payload.model_dump(mode="json"))
