from pydantic import BaseModel
from typing import List

class AutoPlaceRequest(BaseModel):
    category: str
    target_date: str # e.g. "2026-06-20"

class AutoPlaceResponse(BaseModel):
    success: bool
    matched_groups_count: int
    message: str
