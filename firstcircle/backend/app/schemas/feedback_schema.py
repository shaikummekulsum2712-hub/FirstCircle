from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class FeedbackCreate(BaseModel):
    circle_id: int
    user_id: int
    rating: int
    vibe_match: bool = False
    felt_safe: bool = False
    would_meet_again: bool = False
    comment: str = ""

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError("Rating must be between 1 and 5")
        return v


class FeedbackResponse(BaseModel):
    id: int
    circle_id: int
    user_id: int
    rating: int
    vibe_match: bool
    felt_safe: bool
    would_meet_again: bool
    comment: str
    created_at: datetime

    model_config = {"from_attributes": True}
