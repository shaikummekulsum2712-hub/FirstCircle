from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class FreeSlot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(index=True, foreign_key="user.id")

    day_of_week: str
    start_time: str
    end_time: str

    created_at: datetime = Field(default_factory=datetime.utcnow)