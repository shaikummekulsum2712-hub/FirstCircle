from typing import Optional

from sqlmodel import Field, SQLModel


class ProposalParticipant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proposal_id: int = Field(foreign_key="proposal.id")
    user_id: int = Field(foreign_key="user.id")
    response_status: str = Field(default="pending")  # pending, accepted, skipped, expired
