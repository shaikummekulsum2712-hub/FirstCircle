from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Drop(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creator_user_id: int = Field(foreign_key="user.id")
    title: str
    description: str
    circle_type: str  # friend, study, build, random
    location_id: int = Field(foreign_key="location.id")
    scheduled_date: str  # YYYY-MM-DD
    start_time: str  # HH:MM
    end_time: str  # HH:MM
    max_members: int
    current_members: int = Field(default=1)
    status: str = Field(default="open")  # open, full, expired, cancelled
    urgency_level: str  # low, medium, high
    vibe_tags: str = ""  # CSV string for MVP
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
