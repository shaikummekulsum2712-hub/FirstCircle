from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Feedback(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    circle_id: int = Field(foreign_key="circle.id")
    user_id: int = Field(foreign_key="user.id")
    rating: int  # 1-5
    vibe_match: bool = Field(default=False)
    felt_safe: bool = Field(default=False)
    would_meet_again: bool = Field(default=False)
    comment: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
