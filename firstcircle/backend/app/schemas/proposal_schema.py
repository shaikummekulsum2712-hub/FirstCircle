from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any, Optional

class ProposalMemberSummary(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    reliability_score: float
    shared_interests: List[str] = []

class ProposalResponse(BaseModel):
    id: int
    drop_id: int
    drop_title: str
    members_summary: List[ProposalMemberSummary] = []
    votes: Dict[str, str] = {} # e.g. {"1": "accept", "2": "pending"}
    status: str
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class ProposalVote(BaseModel):
    vote: str # 'accept' or 'skip'
