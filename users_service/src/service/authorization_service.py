from fastapi import Request

from core.logging import get_logger
from exception.app_exceptions import AppException
from integration.opa_client import OPAServiceClient
from service.dto.opa_dto import OPAEvaluationRequest

logger = get_logger(__name__)

opa_client = OPAServiceClient()


async def authorize_request(request: Request, role: str, sub: str):
    dto = OPAEvaluationRequest(
        method=request.method,
        path=request.url.path,
        role=role,
        sub = sub,
        request_id=getattr(request.state, "request_id", None)
    )

    logger.debug(f"Input body: {dto}")
    logger.info(f"Trying to send authorization request for {dto}")

    decision = await opa_client.evaluate(dto)

    if not decision:
        raise AppException(
            message="Access denied",
            code="ACCESS_DENIED",
            status_code=403
        )
