import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..utils.security import get_current_user
from ..models.user import User
from ..models.profile import Profile
from ..models.drop import Drop
from ..schemas.proposal_schema import ProposalResponse, ProposalVote, ProposalMemberSummary
from ..services.profile_service import get_profile_by_user_id
from ..services.proposal_service import get_active_proposal_for_profile, vote_on_proposal

router = APIRouter(prefix="/proposals", tags=["proposals"])

@router.get("/active", response_model=ProposalResponse)
def read_active_proposal(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_profile_by_user_id(db, current_user.id)
    proposal = get_active_proposal_for_profile(db, profile.id)
    
    if not proposal:
        raise HTTPException(status_code=404, detail="No active matchmaking proposal found")

    # Fetch details for the Drop
    drop = db.query(Drop).filter(Drop.id == proposal.drop_id).first()
    drop_title = drop.title if drop else "Dynamic Meetup"

    # Decode members
    try:
        member_ids = json.loads(proposal.members_json)
        votes = json.loads(proposal.votes_json)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Data corruption on proposal record")

    # Hydrate blind summaries
    profiles = db.query(Profile).filter(Profile.id.in_(member_ids)).all()
    profile_map = {p.id: p for p in profiles}

    members_summary = []
    
    # Extract all interests to find common overlaps
    all_interests = []
    for pid in member_ids:
        if pid in profile_map and profile_map[pid].interests:
            all_interests.extend([t.strip().lower() for t in profile_map[pid].interests.split(",") if t.strip()])
            
    # Find tags shared by at least 2 members
    from collections import Counter
    interest_counts = Counter(all_interests)
    shared_tags = [tag for tag, count in interest_counts.items() if count >= 2]

    for pid in member_ids:
        if pid in profile_map:
            p = profile_map[pid]
            # Match shared tags for this user
            user_tags = [t.strip().lower() for t in p.interests.split(",") if t.strip()] if p.interests else []
            overlapping = [tag for tag in user_tags if tag in shared_tags]
            
            summary = ProposalMemberSummary(
                age=p.age,
                gender=p.gender,
                reliability_score=p.reliability_score,
                shared_interests=overlapping
            )
            members_summary.append(summary)

    return ProposalResponse(
        id=proposal.id,
        drop_id=proposal.drop_id,
        drop_title=drop_title,
        members_summary=members_summary,
        votes=votes,
        status=proposal.status,
        expires_at=proposal.expires_at,
        created_at=proposal.created_at
    )

@router.post("/{proposal_id}/vote", response_model=ProposalResponse)
def submit_vote(proposal_id: int, payload: ProposalVote, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_profile_by_user_id(db, current_user.id)
    proposal = vote_on_proposal(db, proposal_id, profile.id, payload.vote)
    
    # Call endpoint again to return properly formatted response
    return read_active_proposal(current_user, db)
