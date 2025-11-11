from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ErrorModel(BaseModel):
    message: str
    code: str
    status: int
    requestId: Optional[str]
    timestamp: datetime
