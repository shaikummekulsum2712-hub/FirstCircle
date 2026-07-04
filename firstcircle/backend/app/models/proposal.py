from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Proposal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    drop_id: int = Field(foreign_key="drop.id")
    status: str = Field(default="pending")  # pending, accepted, failed, expired
    required_accept_count: int
    current_accept_count: int = Field(default=0)
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
