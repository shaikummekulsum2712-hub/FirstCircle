from datetime import datetime

from pydantic import BaseModel, field_validator


class VibeVoteCreate(BaseModel):
    drop_id: int
    user_id: int
    vibe_tag: str
    vote_type: str  # up, down

    @field_validator("vote_type")
    @classmethod
    def validate_vote_type(cls, v):
        allowed = {"up", "down"}
        if v not in allowed:
            raise ValueError(f"vote_type must be one of {allowed}")
        return v


class VibeVoteResponse(BaseModel):
    id: int
    drop_id: int
    user_id: int
    vibe_tag: str
    vote_type: str
    created_at: datetime

    model_config = {"from_attributes": True}


class VibeSummaryItem(BaseModel):
    vibe_tag: str
    upvotes: int
    downvotes: int
    net_votes: int


class VibeVoteSummary(BaseModel):
    drop_id: int
    summary: list[VibeSummaryItem]
