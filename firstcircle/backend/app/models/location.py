from typing import Optional

from sqlmodel import Field, SQLModel


class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    location_type: str
    is_safe: bool = True
    allowed_circle_types: str = "friend,study,build,random"