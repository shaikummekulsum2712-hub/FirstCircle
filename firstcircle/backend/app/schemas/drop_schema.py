from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, field_validator


class DropCreate(BaseModel):
    creator_user_id: int
    title: str
    description: str
    circle_type: str
    location_id: int
    scheduled_date: str
    start_time: str
    end_time: str
    max_members: int
    urgency_level: str
    vibe_tags: List[str] = []
    expires_at: datetime

    @field_validator("max_members")
    @classmethod
    def validate_max_members(cls, v):
        if v < 2 or v > 8:
            raise ValueError("max_members must be between 2 and 8")
        return v

    @field_validator("circle_type")
    @classmethod
    def validate_circle_type(cls, v):
        allowed = {"friend", "study", "build", "random"}
        if v not in allowed:
            raise ValueError(f"circle_type must be one of {allowed}")
        return v

    @field_validator("urgency_level")
    @classmethod
    def validate_urgency_level(cls, v):
        allowed = {"low", "medium", "high"}
        if v not in allowed:
            raise ValueError(f"urgency_level must be one of {allowed}")
        return v


class DropResponse(BaseModel):
    id: int
    creator_user_id: int
    title: str
    description: str
    circle_type: str
    location_id: int
    scheduled_date: str
    start_time: str
    end_time: str
    max_members: int
    current_members: int
    status: str
    urgency_level: str
    vibe_tags: List[str]
    created_at: datetime
    expires_at: datetime

    model_config = {"from_attributes": True}
