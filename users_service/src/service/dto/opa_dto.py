from pydantic import BaseModel
from typing import Optional

class OPAEvaluationRequest(BaseModel):
    method: str
    path: str
    role: str
    sub: str
    request_id: Optional[str] = None
