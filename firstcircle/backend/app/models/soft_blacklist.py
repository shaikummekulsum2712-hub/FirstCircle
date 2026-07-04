from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class SoftBlacklist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    blocked_user_id: int = Field(foreign_key="user.id")
    reason: str
    expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
