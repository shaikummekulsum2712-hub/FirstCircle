from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class DropMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    drop_id: int = Field(foreign_key="drop.id")
    user_id: int = Field(foreign_key="user.id")
    role: str  # creator, member
    join_status: str  # joined, left, removed
    joined_at: datetime = Field(default_factory=datetime.utcnow)
