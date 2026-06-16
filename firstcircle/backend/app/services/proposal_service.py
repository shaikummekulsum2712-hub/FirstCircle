import json
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import HTTPException
from ..models.proposal import Proposal
from ..models.drop import Drop
from ..models.profile import Profile
from ..models.circle import Circle
from ..models.drop_member import DropMember
from ..models.soft_blacklist import SoftBlacklist
from ..schemas.proposal_schema import ProposalResponse, ProposalMemberSummary

def get_active_proposal_for_profile(db: Session, profile_id: int) -> Optional[Proposal]:
    """
    Returns the active proposal where this profile is a proposed member.
    """
    proposals = db.query(Proposal).filter(Proposal.status == "pending").all()
    for p in proposals:
        try:
            members = json.loads(p.members_json)
            if profile_id in members:
                return p
        except json.JSONDecodeError:
            pass
    return None

def vote_on_proposal(db: Session, proposal_id: int, profile_id: int, vote: str) -> Proposal:
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal or proposal.status != "pending":
        raise HTTPException(status_code=400, detail="No active proposal found")

    try:
        members = json.loads(proposal.members_json)
        votes = json.loads(proposal.votes_json)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Data parsing error")

    if profile_id not in members:
        raise HTTPException(status_code=403, detail="Not authorized to vote on this proposal")

    # Save vote
    votes[str(profile_id)] = vote
    proposal.votes_json = json.dumps(votes)

    # If any member rejects/skips: the proposal is failed/skipped
    if vote == "skip":
        proposal.status = "skipped"
        # Revert drop status to open so matching can run again
        drop = db.query(Drop).filter(Drop.id == proposal.drop_id).first()
        if drop:
            drop.status = "open"
            
        # Add to soft blacklist so we don't match the skipper with these users again
        for m_id in members:
            if m_id != profile_id:
                # Add mutual soft blacklists
                sb1 = SoftBlacklist(user_id=profile_id, blacklisted_user_id=m_id)
                sb2 = SoftBlacklist(user_id=m_id, blacklisted_user_id=profile_id)
                db.add(sb1)
                db.add(sb2)
        db.commit()
        return proposal

    # Check if all members accepted
    all_accepted = all(votes.get(str(m_id)) == "accept" for m_id in members)
    if all_accepted:
        proposal.status = "accepted"
        
        # Create Confirmed Circle
        drop = db.query(Drop).filter(Drop.id == proposal.drop_id).first()
        if drop:
            new_circle = Circle(
                drop_id=drop.id,
                title=f"{drop.title} Circle",
                event_time=drop.event_time,
                location_name=drop.location_name,
                status="scheduled"
            )
            db.add(new_circle)
            drop.status = "completed"  # Mark drop matching complete

    db.commit()
    db.refresh(proposal)
    return proposal
