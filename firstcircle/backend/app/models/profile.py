from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(index=True, foreign_key="user.id")

    year: str
    branch: str
    student_type: str
    bio: str = ""

    # Stored as comma-separated strings for MVP simplicity.
    # Later we can normalize or use JSON/PostgreSQL arrays.
    interests: str = ""
    comfort_preferences: str = ""
    skills: str = ""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)