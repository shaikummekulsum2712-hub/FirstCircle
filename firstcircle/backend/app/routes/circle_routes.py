from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..utils.security import get_current_user
from ..models.user import User
from ..schemas.circle_schema import CircleResponse, RescheduleRequest
from ..services.profile_service import get_profile_by_user_id
from ..services.circle_service import get_active_circles_for_profile, get_circle_history_for_profile, get_circle_by_id, request_circle_reschedule

router = APIRouter(prefix="/circles", tags=["circles"])

@router.get("/active", response_model=List[CircleResponse])
def get_active_circles(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_profile_by_user_id(db, current_user.id)
    circles = get_active_circles_for_profile(db, profile.id)
    
    # Hydrate members for response validation
    result = []
    for c in circles:
        hydrated = get_circle_by_id(db, c.id, profile.id)
        result.append(hydrated)
    return result

@router.get("/history", response_model=List[CircleResponse])
def get_circle_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_profile_by_user_id(db, current_user.id)
    circles = get_circle_history_for_profile(db, profile.id)
    
    result = []
    for c in circles:
        hydrated = get_circle_by_id(db, c.id, profile.id)
        result.append(hydrated)
    return result

@router.get("/{circle_id}", response_model=CircleResponse)
def get_circle(circle_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_profile_by_user_id(db, current_user.id)
    return get_circle_by_id(db, circle_id, profile.id)

@router.post("/{circle_id}/reschedule", response_model=CircleResponse)
def reschedule(circle_id: int, payload: RescheduleRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_profile_by_user_id(db, current_user.id)
    return request_circle_reschedule(db, circle_id, profile.id, payload.proposed_time)
