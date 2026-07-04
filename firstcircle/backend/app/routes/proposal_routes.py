"""Proposal routes for blind proposals."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.schemas.proposal_schema import ProposalCreate, ProposalResponse, ProposalDetailResponse
from app.services.proposal_service import (
    create_proposal,
    get_proposal,
    accept_proposal,
    skip_proposal,
    expire_proposal,
    get_user_proposals,
)

router = APIRouter(prefix="/api/proposals", tags=["proposals"])


@router.post("/drop/{drop_id}", response_model=ProposalResponse)
def create_proposal_endpoint(
    drop_id: int,
    required_accept_count: int,
    session: Session = Depends(get_session),
):
    """Create a blind proposal for a drop."""
    proposal = create_proposal(drop_id, required_accept_count, session)
    return proposal


@router.get("/{proposal_id}", response_model=ProposalDetailResponse)
def get_proposal_endpoint(proposal_id: int, session: Session = Depends(get_session)):
    """Get proposal details by ID."""
    proposal = get_proposal(proposal_id, session)

    # Get participant count
    from app.models.proposal_participant import ProposalParticipant
    from sqlmodel import select

    participants = session.exec(
        select(ProposalParticipant).where(ProposalParticipant.proposal_id == proposal_id)
    ).all()

    return ProposalDetailResponse(
        id=proposal.id,
        drop_id=proposal.drop_id,
        status=proposal.status,
        required_accept_count=proposal.required_accept_count,
        current_accept_count=proposal.current_accept_count,
        participant_count=len(participants),
        expires_at=proposal.expires_at,
        created_at=proposal.created_at,
    )


@router.patch("/{proposal_id}/accept", response_model=ProposalResponse)
def accept_proposal_endpoint(
    proposal_id: int,
    user_id: int,
    session: Session = Depends(get_session),
):
    """User accepts the proposal."""
    proposal = accept_proposal(proposal_id, user_id, session)
    return proposal


@router.patch("/{proposal_id}/skip", response_model=dict)
def skip_proposal_endpoint(
    proposal_id: int,
    user_id: int,
    session: Session = Depends(get_session),
):
    """User skips the proposal."""
    result = skip_proposal(proposal_id, user_id, session)
    return result


@router.patch("/{proposal_id}/expire", response_model=ProposalResponse)
def expire_proposal_endpoint(
    proposal_id: int, session: Session = Depends(get_session)
):
    """Expire a proposal."""
    proposal = expire_proposal(proposal_id, session)
    return proposal


@router.get("/user/{user_id}", response_model=list[ProposalResponse])
def get_user_proposals_endpoint(
    user_id: int, session: Session = Depends(get_session)
):
    """Get all proposals a user participates in."""
    proposals = get_user_proposals(user_id, session)
    return proposals
