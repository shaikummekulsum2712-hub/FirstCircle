from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    circle_id: int = Field(foreign_key="circle.id")
    reporter_user_id: int = Field(foreign_key="user.id")
    reported_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    reason: str
    details: str = ""
    status: str = Field(default="open")  # open, reviewed, resolved
    created_at: datetime = Field(default_factory=datetime.utcnow)
