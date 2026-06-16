from pydantic import BaseModel, Field
from typing import List, Optional

class FreeSlotBase(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6) # 0 = Monday, 6 = Sunday
    start_time: str = Field(..., pattern="^[0-2][0-9]:[0-5][0-9]$") # "HH:MM"
    end_time: str = Field(..., pattern="^[0-2][0-9]:[0-5][0-9]$") # "HH:MM"

class FreeSlotCreate(FreeSlotBase):
    pass

class FreeSlotResponse(FreeSlotBase):
    id: int
    profile_id: int

    class Config:
        from_attributes = True

class ProfileBase(BaseModel):
    display_name: str
    bio: Optional[str] = None
    age: Optional[int] = Field(None, ge=18, le=120)
    gender: Optional[str] = None
    interests: Optional[str] = None # Comma-separated
    comforts: Optional[str] = None   # JSON formatted preferences

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    reliability_score: float
    free_slots: List[FreeSlotResponse] = []

    class Config:
        from_attributes = True
