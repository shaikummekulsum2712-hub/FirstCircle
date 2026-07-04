"""Proposal service for blind proposals."""

from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.drop import Drop
from app.models.proposal import Proposal
from app.models.proposal_participant import ProposalParticipant
from app.models.user import User


def create_proposal(drop_id: int, required_accept_count: int, session: Session) -> Proposal:
    """
    Create a proposal for a drop.
    
    Include current joined members as participants.
    """
    # Validate drop exists
    drop = session.get(Drop, drop_id)
    if not drop:
        raise HTTPException(status_code=404, detail="Drop not found")

    # Get current members from drop_members
    from app.models.drop_member import DropMember
    members = session.exec(
        select(DropMember).where(
            DropMember.drop_id == drop_id,
            DropMember.join_status == "joined",
        )
    ).all()

    if len(members) == 0:
        raise HTTPException(status_code=400, detail="Drop has no members")

    # Create proposal
    proposal = Proposal(
        drop_id=drop_id,
        required_accept_count=required_accept_count,
        current_accept_count=0,
        expires_at=datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0),  # Tomorrow midnight
    )
    session.add(proposal)
    session.commit()
    session.refresh(proposal)

    # Create participants
    for member in members:
        participant = ProposalParticipant(
            proposal_id=proposal.id,
            user_id=member.user_id,
            response_status="pending",
        )
        session.add(participant)

    session.commit()
    return proposal


def get_proposal(proposal_id: int, session: Session) -> Proposal:
    """Get a proposal by ID."""
    proposal = session.get(Proposal, proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal


def accept_proposal(proposal_id: int, user_id: int, session: Session) -> Proposal:
    """
    User accepts a proposal.
    
    Increases current_accept_count.
    If enough accept, proposal status becomes accepted.
    """
    # Validate user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get proposal
    proposal = get_proposal(proposal_id, session)

    # Check if user is a participant
    participant = session.exec(
        select(ProposalParticipant).where(
            ProposalParticipant.proposal_id == proposal_id,
            ProposalParticipant.user_id == user_id,
        )
    ).first()

    if not participant:
        raise HTTPException(status_code=400, detail="User is not a participant in this proposal")

    # Check if already responded
    if participant.response_status != "pending":
        raise HTTPException(status_code=400, detail="User already responded to this proposal")

    # Mark as accepted
    participant.response_status = "accepted"
    session.add(participant)

    # Increment accept count
    proposal.current_accept_count += 1

    # Check if required count reached
    if proposal.current_accept_count >= proposal.required_accept_count:
        proposal.status = "accepted"

    session.add(proposal)
    session.commit()
    session.refresh(proposal)
    return proposal


def skip_proposal(proposal_id: int, user_id: int, session: Session) -> dict:
    """
    User skips a proposal.
    
    Creates soft blacklist entries between skipper and other participants.
    """
    # Validate user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get proposal
    proposal = get_proposal(proposal_id, session)

    # Check if user is a participant
    participant = session.exec(
        select(ProposalParticipant).where(
            ProposalParticipant.proposal_id == proposal_id,
            ProposalParticipant.user_id == user_id,
        )
    ).first()

    if not participant:
        raise HTTPException(status_code=400, detail="User is not a participant in this proposal")

    # Check if already responded
    if participant.response_status != "pending":
        raise HTTPException(status_code=400, detail="User already responded to this proposal")

    # Mark as skipped
    participant.response_status = "skipped"
    session.add(participant)

    # Create soft blacklist entries with other participants
    other_participants = session.exec(
        select(ProposalParticipant).where(
            ProposalParticipant.proposal_id == proposal_id,
            ProposalParticipant.user_id != user_id,
        )
    ).all()

    from app.models.soft_blacklist import SoftBlacklist

    for other in other_participants:
        # Blacklist skipper from other
        blacklist = SoftBlacklist(
            user_id=other.user_id,
            blocked_user_id=user_id,
            reason="Skip proposal",
        )
        session.add(blacklist)

    session.commit()
    return {"message": "Proposal skipped, soft blacklist created"}


def expire_proposal(proposal_id: int, session: Session) -> Proposal:
    """Mark proposal as expired."""
    proposal = get_proposal(proposal_id, session)

    # Mark all pending participants as expired
    participants = session.exec(
        select(ProposalParticipant).where(
            ProposalParticipant.proposal_id == proposal_id,
            ProposalParticipant.response_status == "pending",
        )
    ).all()

    for p in participants:
        p.response_status = "expired"
        session.add(p)

    proposal.status = "expired"
    session.add(proposal)
    session.commit()
    session.refresh(proposal)
    return proposal


def get_user_proposals(user_id: int, session: Session) -> list[Proposal]:
    """Get all proposals a user participates in."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all participant entries for this user
    participants = session.exec(
        select(ProposalParticipant).where(ProposalParticipant.user_id == user_id)
    ).all()

    # Get unique proposal IDs
    proposal_ids = set([p.proposal_id for p in participants])

    # Get proposals
    proposals = []
    for pid in proposal_ids:
        proposal = session.get(Proposal, pid)
        if proposal:
            proposals.append(proposal)

    return proposals
