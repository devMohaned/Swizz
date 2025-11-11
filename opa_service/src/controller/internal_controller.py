from fastapi import APIRouter
from service.dto.policy_dto import PolicyInput, PolicyDecision
from service.policy_service import PolicyService

router = APIRouter(prefix="/api/internal", tags=["Policy Evaluation"])
service = PolicyService()

@router.post("/evaluate", response_model=PolicyDecision)
async def evaluate_policy(policy_input: PolicyInput):
    return await service.evaluate_policy(policy_input)
