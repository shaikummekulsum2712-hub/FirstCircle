from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException
from ..models.circle import Circle
from ..models.drop_member import DropMember
from ..models.profile import Profile
from ..models.proposal import Proposal
import json

def get_active_circles_for_profile(db: Session, profile_id: int) -> List[Circle]:
    """
    Returns circles that the user belongs to (checked via the proposal members list).
    """
    circles = db.query(Circle).filter(Circle.status.in_(["scheduled", "rescheduled"])).all()
    user_circles = []
    
    for c in circles:
        # Load the proposal for this circle's drop
        proposal = db.query(Proposal).filter(
            Proposal.drop_id == c.drop_id,
            Proposal.status == "accepted"
        ).first()
        if proposal:
            try:
                members = json.loads(proposal.members_json)
                if profile_id in members:
                    user_circles.append(c)
            except json.JSONDecodeError:
                pass
                
    return user_circles

def get_circle_history_for_profile(db: Session, profile_id: int) -> List[Circle]:
    circles = db.query(Circle).filter(Circle.status == "completed").all()
    user_circles = []
    
    for c in circles:
        proposal = db.query(Proposal).filter(
            Proposal.drop_id == c.drop_id,
            Proposal.status == "accepted"
        ).first()
        if proposal:
            try:
                members = json.loads(proposal.members_json)
                if profile_id in members:
                    user_circles.append(c)
            except json.JSONDecodeError:
                pass
                
    return user_circles

def get_circle_by_id(db: Session, circle_id: int, profile_id: int) -> Circle:
    circle = db.query(Circle).filter(Circle.id == circle_id).first()
    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")

    proposal = db.query(Proposal).filter(
        Proposal.drop_id == circle.drop_id,
        Proposal.status == "accepted"
    ).first()
    
    if not proposal:
        raise HTTPException(status_code=400, detail="Circle match record not found")
        
    try:
        members = json.loads(proposal.members_json)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Data parsing error")

    if profile_id not in members:
        raise HTTPException(status_code=403, detail="Access denied")

    # Inject members into circle object dynamically for routers
    profiles = db.query(Profile).filter(Profile.id.in_(members)).all()
    circle.members = profiles
    return circle

def request_circle_reschedule(db: Session, circle_id: int, profile_id: int, new_time: datetime) -> Circle:
    circle = db.query(Circle).filter(Circle.id == circle_id).first()
    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")

    # Check authorization
    proposal = db.query(Proposal).filter(
        Proposal.drop_id == circle.drop_id,
        Proposal.status == "accepted"
    ).first()
    if not proposal:
        raise HTTPException(status_code=400, detail="Matching proposal not found")

    try:
        members = json.loads(proposal.members_json)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Database error")

    if profile_id not in members:
        raise HTTPException(status_code=403, detail="Unauthorized")

    circle.event_time = new_time
    circle.status = "rescheduled"
    db.commit()
    db.refresh(circle)
    return circle
