from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas.profile_schema import ProfileCreate, ProfileRead, ProfileUpdate
from app.services.profile_service import (
    create_profile,
    get_profile_by_user_id,
    update_profile,
)

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("/", response_model=ProfileRead)
def create_student_profile(
    profile_data: ProfileCreate,
    session: Session = Depends(get_session),
):
    return create_profile(session, profile_data)


@router.get("/user/{user_id}", response_model=ProfileRead)
def get_student_profile(
    user_id: int,
    session: Session = Depends(get_session),
):
    return get_profile_by_user_id(session, user_id)


@router.put("/user/{user_id}", response_model=ProfileRead)
def update_student_profile(
    user_id: int,
    profile_data: ProfileUpdate,
    session: Session = Depends(get_session),
):
    return update_profile(session, user_id, profile_data)