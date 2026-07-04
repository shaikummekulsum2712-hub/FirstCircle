from pydantic import BaseModel


class FreeSlotCreate(BaseModel):
    user_id: int
    day_of_week: str
    start_time: str
    end_time: str


class FreeSlotRead(BaseModel):
    id: int
    user_id: int
    day_of_week: str
    start_time: str
    end_time: str

    class Config:
        from_attributes = True