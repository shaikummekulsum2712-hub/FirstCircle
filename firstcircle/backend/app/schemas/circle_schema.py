from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CircleMemberDetail(BaseModel):
    profile_id: int
    display_name: str
    bio: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    reliability_score: float
    interests: Optional[str] = None

class CircleResponse(BaseModel):
    id: int
    drop_id: int
    title: str
    event_time: datetime
    location_name: str
    status: str
    created_at: datetime
    members: List[CircleMemberDetail] = []

    class Config:
        from_attributes = True

class RescheduleRequest(BaseModel):
    proposed_time: datetime
