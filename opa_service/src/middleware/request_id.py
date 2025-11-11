import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from .request_context import set_request_id


class RequestIdMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
        request.state.request_id = request_id
        set_request_id(request_id)

        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
