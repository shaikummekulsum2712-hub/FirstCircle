from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class DropBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    event_time: datetime
    location_name: str
    max_members: int = Field(5, ge=3, le=10)

class DropCreate(DropBase):
    pass

class DropMemberResponse(BaseModel):
    profile_id: int
    joined_at: datetime
    display_name: str

    class Config:
        from_attributes = True

class VibeVoteCreate(BaseModel):
    vibe_value: str = Field(..., pattern="^(chill|active|party|intellectual)$")

class DropResponse(DropBase):
    id: int
    host_id: int
    status: str
    created_at: datetime
    members: List[DropMemberResponse] = []

    class Config:
        from_attributes = True
