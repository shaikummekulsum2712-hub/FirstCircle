from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Circle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    drop_id: int = Field(foreign_key="drop.id")
    proposal_id: int = Field(foreign_key="proposal.id")
    status: str = Field(default="confirmed")  # confirmed, completed, cancelled
    meeting_place: str
    meeting_date: str  # YYYY-MM-DD
    start_time: str  # HH:MM
    end_time: str  # HH:MM
    created_at: datetime = Field(default_factory=datetime.utcnow)
