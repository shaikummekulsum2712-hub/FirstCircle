from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReportCreate(BaseModel):
    circle_id: int
    reporter_user_id: int
    reported_user_id: Optional[int] = None
    reason: str
    details: str = ""


class ReportResponse(BaseModel):
    id: int
    circle_id: int
    reporter_user_id: int
    reported_user_id: Optional[int]
    reason: str
    details: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
