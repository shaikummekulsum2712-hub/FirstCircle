from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ProposalParticipantResponse(BaseModel):
    id: int
    proposal_id: int
    user_id: int
    response_status: str

    model_config = {"from_attributes": True}


class ProposalCreate(BaseModel):
    drop_id: int
    required_accept_count: int


class ProposalResponse(BaseModel):
    id: int
    drop_id: int
    status: str
    required_accept_count: int
    current_accept_count: int
    expires_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class ProposalDetailResponse(BaseModel):
    id: int
    drop_id: int
    status: str
    required_accept_count: int
    current_accept_count: int
    participant_count: int
    expires_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
