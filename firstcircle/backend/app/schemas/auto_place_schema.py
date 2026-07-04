from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class AutoPlaceRequest(BaseModel):
    user_id: int
    preferred_circle_type: str  # friend, study, build, random, any
    preferred_day: str  # YYYY-MM-DD
    preferred_start_time: str  # HH:MM
    preferred_end_time: str  # HH:MM
    preferred_vibes: List[str] = []


class ScoreBreakdown(BaseModel):
    circle_type_fit: float
    time_fit: float
    profile_fit: float
    vibe_fit: float
    urgency_boost: float
    fairness_boost: float
    total: float


class DropRecommendation(BaseModel):
    drop_id: int
    title: str
    description: str
    circle_type: str
    scheduled_date: str
    start_time: str
    end_time: str
    location_id: int
    current_members: int
    max_members: int
    creator_user_id: int
    vibe_tags: List[str]


class AutoPlaceResponse(BaseModel):
    recommended_drop: Optional[DropRecommendation]
    score: Optional[float]
    score_breakdown: Optional[ScoreBreakdown]
    reason: str
