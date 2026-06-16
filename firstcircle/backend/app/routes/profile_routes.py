from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..utils.security import get_current_user
from ..models.user import User
from ..schemas.profile_schema import ProfileResponse, ProfileUpdate, FreeSlotCreate, FreeSlotResponse
from ..services.profile_service import get_profile_by_user_id, update_profile, set_profile_slots, get_profile_slots

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/me", response_model=ProfileResponse)
def read_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_profile_by_user_id(db, current_user.id)

@router.put("/me", response_model=ProfileResponse)
def edit_profile(profile_data: ProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_profile_by_user_id(db, current_user.id)
    return update_profile(db, profile, profile_data)

@router.get("/slots", response_model=List[FreeSlotResponse])
def read_slots(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_profile_by_user_id(db, current_user.id)
    return get_profile_slots(db, profile.id)

@router.post("/slots", response_model=List[FreeSlotResponse])
def save_slots(slots: List[FreeSlotCreate], current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_profile_by_user_id(db, current_user.id)
    return set_profile_slots(db, profile.id, slots)
