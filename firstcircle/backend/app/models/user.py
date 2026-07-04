from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    email: str = Field(index=True, unique=True)
    roll_number: str = Field(index=True, unique=True)

    college_domain: str
    email_verified: bool = False

    verification_status: str = "pending"
    # pending / email_verified / manually_verified / officially_verified / rejected

    created_at: datetime = Field(default_factory=datetime.utcnow)