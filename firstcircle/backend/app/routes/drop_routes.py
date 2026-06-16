from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..utils.security import get_current_user
from ..models.user import User
from ..schemas.drop_schema import DropCreate, DropResponse, VibeVoteCreate
from ..services.profile_service import get_profile_by_user_id
from ..services.drop_service import create_drop, get_active_drops, join_drop, vote_drop_vibe, trigger_matching_for_drop, get_drop_by_id

router = APIRouter(prefix="/drops", tags=["drops"])

@router.post("", response_model=DropResponse, status_code=status.HTTP_201_CREATED)
def post_drop(drop_data: DropCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_profile_by_user_id(db, current_user.id)
    return create_drop(db, profile.id, drop_data)

@router.get("", response_model=List[DropResponse])
def get_drops(category: Optional[str] = Query(None), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_active_drops(db, category)

@router.post("/{drop_id}/join", status_code=status.HTTP_200_OK)
def join(drop_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_profile_by_user_id(db, current_user.id)
    join_drop(db, drop_id, profile.id)
    return {"message": "Successfully joined drop"}

@router.post("/{drop_id}/vibe-vote", status_code=status.HTTP_200_OK)
def vote_vibe(drop_id: int, vote: VibeVoteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_profile_by_user_id(db, current_user.id)
    vote_drop_vibe(db, drop_id, profile.id, vote.vibe_value)
    return {"message": "Vibe vote submitted"}

@router.post("/{drop_id}/match", status_code=status.HTTP_200_OK)
def manual_match(drop_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Run matchmaking matching
    proposal = trigger_matching_for_drop(db, drop_id)
    if not proposal:
        return {"success": False, "message": "Could not form a matching group. Ensure there are at least 3 members with schedule overlaps."}
    return {"success": True, "message": f"Proposal {proposal.id} created successfully."}
