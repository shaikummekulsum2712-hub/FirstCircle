from pydantic import BaseModel, Field
from typing import List, Optional

class AttendanceConfirmation(BaseModel):
    profile_id: int
    status: str = Field(..., pattern="^(on-time|late|no-show)$")

class PeerRating(BaseModel):
    profile_id: int
    rating: int = Field(..., ge=1, le=5)
    tags: Optional[str] = None # comma separated tags like "friendly,helpful"

class FeedbackCreate(BaseModel):
    circle_id: int
    attendance: List[AttendanceConfirmation]
    ratings: List[PeerRating]

class ReportCreate(BaseModel):
    circle_id: int
    reportee_id: int
    reason: str
