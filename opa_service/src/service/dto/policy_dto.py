from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PolicyInput(BaseModel):
    method: str
    path: str
    role: str
    sub: str
    request_id: Optional[str] = None

class PolicyDecision(BaseModel):
    allow: bool
    policy: str = "user_access"
    timestamp: datetime
    decision_id: Optional[str] = None
