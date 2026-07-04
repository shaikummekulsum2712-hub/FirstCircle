from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CircleMemberResponse(BaseModel):
    id: int
    circle_id: int
    user_id: int
    attendance_status: str
    revealed: bool

    model_config = {"from_attributes": True}


class CircleCreate(BaseModel):
    proposal_id: int
    meeting_place: str
    meeting_date: str
    start_time: str
    end_time: str


class CircleResponse(BaseModel):
    id: int
    drop_id: int
    proposal_id: int
    status: str
    meeting_place: str
    meeting_date: str
    start_time: str
    end_time: str
    created_at: datetime

    model_config = {"from_attributes": True}
