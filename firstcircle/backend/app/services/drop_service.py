from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from fastapi import HTTPException, status
from ..models.drop import Drop
from ..models.drop_member import DropMember
from ..models.vibe_vote import VibeVote
from ..models.free_slot import FreeSlot
from ..models.profile import Profile
from ..models.proposal import Proposal
from ..schemas.drop_schema import DropCreate
from ..matching.group_builder import build_best_matching_group

def create_drop(db: Session, host_profile_id: int, drop_data: DropCreate) -> Drop:
    new_drop = Drop(
        host_id=host_profile_id,
        title=drop_data.title,
        description=drop_data.description,
        category=drop_data.category,
        event_time=drop_data.event_time,
        location_name=drop_data.location_name,
        max_members=drop_data.max_members,
        status="open"
    )
    db.add(new_drop)
    db.commit()
    db.refresh(new_drop)

    # Host joins by default
    join_drop(db, new_drop.id, host_profile_id)
    return new_drop

def get_active_drops(db: Session, category: Optional[str] = None) -> List[Drop]:
    query = db.query(Drop).filter(Drop.status == "open")
    if category:
        query = query.filter(Drop.category == category)
    return query.all()

def get_drop_by_id(db: Session, drop_id: int) -> Optional[Drop]:
    return db.query(Drop).filter(Drop.id == drop_id).first()

def join_drop(db: Session, drop_id: int, profile_id: int) -> DropMember:
    drop = get_drop_by_id(db, drop_id)
    if not drop:
        raise HTTPException(status_code=404, detail="Drop not found")
    if drop.status != "open":
        raise HTTPException(status_code=400, detail="Cannot join a closed drop")

    # Check if already joined
    existing = db.query(DropMember).filter(
        DropMember.drop_id == drop_id,
        DropMember.profile_id == profile_id
    ).first()
    if existing:
        return existing

    new_member = DropMember(drop_id=drop_id, profile_id=profile_id)
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

def vote_drop_vibe(db: Session, drop_id: int, profile_id: int, vibe: str) -> VibeVote:
    existing = db.query(VibeVote).filter(
        VibeVote.drop_id == drop_id,
        VibeVote.profile_id == profile_id
    ).first()
    
    if existing:
        existing.vibe_value = vibe
        db.commit()
        db.refresh(existing)
        return existing
        
    vote = VibeVote(drop_id=drop_id, profile_id=profile_id, vibe_value=vibe)
    db.add(vote)
    db.commit()
    db.refresh(vote)
    return vote

def trigger_matching_for_drop(db: Session, drop_id: int) -> Optional[Proposal]:
    """
    Orchestrates the matching engine to find a group for the drop.
    If match is found, creates a blind Proposal.
    """
    drop = get_drop_by_id(db, drop_id)
    if not drop or drop.status != "open":
        return None

    # Get joined members
    members = db.query(DropMember).filter(DropMember.drop_id == drop_id).all()
    member_profiles = [db.query(Profile).filter(Profile.id == m.profile_id).first() for m in members]
    member_ids = [p.id for p in member_profiles if p]

    if len(member_ids) < 3:
        # Not enough members to form a circle
        return None

    # Load free slots for these profiles
    slots = db.query(FreeSlot).filter(FreeSlot.profile_id.in_(member_ids)).all()
    slots_by_user: Dict[int, List[FreeSlot]] = {pid: [] for pid in member_ids}
    for s in slots:
        slots_by_user[s.profile_id].append(s)

    # Run group builder
    best_group, score = build_best_matching_group(
        db, member_profiles, slots_by_user, min_size=3, max_size=drop.max_members
    )

    if not best_group:
        return None

    # Create Proposal
    votes = {str(pid): "pending" for pid in best_group}
    new_proposal = Proposal(
        drop_id=drop_id,
        members_json=str(best_group),
        votes_json=str(votes).replace("'", '"'),
        status="pending",
        expires_at=datetime.utcnow() + timedelta(hours=2) # 2 hours countdown standard
    )
    db.add(new_proposal)

    # Set drop status to matching
    drop.status = "matching"
    db.commit()
    db.refresh(new_proposal)
    return new_proposal
