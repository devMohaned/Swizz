import logging

import httpx

from config.settings import settings
from service.dto.opa_dto import OPAEvaluationRequest

logger = logging.getLogger(__name__)


class OPAServiceClient:
    def __init__(self):
        self.url = settings.opa_service_url

    async def evaluate(self, payload: OPAEvaluationRequest) -> bool:
        headers = {}
        if payload.request_id:
            headers["X-Request-ID"] = payload.request_id

        try:
            async with httpx.AsyncClient(timeout=settings.timeout) as client:
                resp = await client.post(self.url, json=payload.model_dump(mode="json"), headers=headers)
                resp.raise_for_status()
                data = resp.json()
                decision = data.get("allow", False)
                logger.info(f"OPA decision from internal API: {decision} for {payload}")
                return decision
        except Exception as e:
            logger.exception("Failed to reach internal OPA microservice")
            raise
