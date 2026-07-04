from typing import Optional

from sqlmodel import Field, SQLModel


class Reliability(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    completed_circles: int = Field(default=0)
    no_shows: int = Field(default=0)
    reports_received: int = Field(default=0)
    reliability_score: float = Field(default=5.0)  # Out of 5
