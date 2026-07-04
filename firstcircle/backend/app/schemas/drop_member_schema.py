from datetime import datetime

from pydantic import BaseModel


class DropMemberJoin(BaseModel):
    drop_id: int
    user_id: int


class DropMemberLeave(BaseModel):
    drop_id: int
    user_id: int


class DropMemberResponse(BaseModel):
    id: int
    drop_id: int
    user_id: int
    role: str
    join_status: str
    joined_at: datetime

    model_config = {"from_attributes": True}
