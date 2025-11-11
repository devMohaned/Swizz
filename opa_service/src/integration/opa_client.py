import httpx
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class OPAClient:
    def __init__(self):
        self.url = settings.opa_url

    async def evaluate(self, payload: dict) -> bool:
        try:
            async with httpx.AsyncClient(timeout=settings.timeout) as client:
                resp = await client.post(self.url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                decision = data.get("result", False)
                logger.info(f"OPA decision: {decision} for {payload}")
                return bool(decision)
        except Exception as e:
            logger.exception("Failed to reach OPA service")
            raise
