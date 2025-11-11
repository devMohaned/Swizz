import uuid
from datetime import datetime, UTC

from core.logging import get_logger
from integration.opa_client import OPAClient
from service.dto.policy_dto import PolicyInput, PolicyDecision

logger = get_logger(__name__)


class PolicyService:
    def __init__(self):
        self.opa_client = OPAClient()

    async def evaluate_policy(self, policy_input: PolicyInput) -> PolicyDecision:
        logger.info(f"Evaluating policy: {policy_input}")
        payload = {"input": policy_input.model_dump(mode="json")}
        allow = await self.opa_client.evaluate(payload)
        return PolicyDecision(
            allow=allow,
            timestamp=datetime.now(UTC),
            decision_id=str(uuid.uuid4())
        )
