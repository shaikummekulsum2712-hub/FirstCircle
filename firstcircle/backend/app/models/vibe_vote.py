from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class VibeVote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    drop_id: int = Field(foreign_key="drop.id")
    user_id: int = Field(foreign_key="user.id")
    vibe_tag: str
    vote_type: str  # up, down
    created_at: datetime = Field(default_factory=datetime.utcnow)
