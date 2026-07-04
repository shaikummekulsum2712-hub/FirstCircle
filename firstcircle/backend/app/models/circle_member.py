from typing import Optional

from sqlmodel import Field, SQLModel


class CircleMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    circle_id: int = Field(foreign_key="circle.id")
    user_id: int = Field(foreign_key="user.id")
    attendance_status: str = Field(default="unknown")  # unknown, attended, no_show
    revealed: bool = Field(default=False)
