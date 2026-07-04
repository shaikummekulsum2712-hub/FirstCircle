from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.profile import Profile
from app.models.user import User
from app.schemas.profile_schema import ProfileCreate, ProfileRead, ProfileUpdate
from app.utils.validators import csv_to_list, list_to_csv


def profile_to_read(profile: Profile) -> ProfileRead:
    return ProfileRead(
        id=profile.id,
        user_id=profile.user_id,
        year=profile.year,
        branch=profile.branch,
        student_type=profile.student_type,
        bio=profile.bio,
        interests=csv_to_list(profile.interests),
        comfort_preferences=csv_to_list(profile.comfort_preferences),
        skills=csv_to_list(profile.skills),
    )


def create_profile(session: Session, profile_data: ProfileCreate) -> ProfileRead:
    user = session.get(User, profile_data.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_profile = session.exec(
        select(Profile).where(Profile.user_id == profile_data.user_id)
    ).first()

    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists for this user")

    profile = Profile(
        user_id=profile_data.user_id,
        year=profile_data.year,
        branch=profile_data.branch,
        student_type=profile_data.student_type,
        bio=profile_data.bio,
        interests=list_to_csv(profile_data.interests),
        comfort_preferences=list_to_csv(profile_data.comfort_preferences),
        skills=list_to_csv(profile_data.skills),
    )

    session.add(profile)
    session.commit()
    session.refresh(profile)

    return profile_to_read(profile)


def get_profile_by_user_id(session: Session, user_id: int) -> ProfileRead:
    profile = session.exec(
        select(Profile).where(Profile.user_id == user_id)
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile_to_read(profile)


def update_profile(
    session: Session,
    user_id: int,
    profile_data: ProfileUpdate,
) -> ProfileRead:
    profile = session.exec(
        select(Profile).where(Profile.user_id == user_id)
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    update_data = profile_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "interests" and value is not None:
          profile.interests = list_to_csv(value)
        elif key == "comfort_preferences" and value is not None:
          profile.comfort_preferences = list_to_csv(value)
        elif key == "skills" and value is not None:
          profile.skills = list_to_csv(value)
        elif value is not None:
          setattr(profile, key, value)

    profile.updated_at = datetime.utcnow()

    session.add(profile)
    session.commit()
    session.refresh(profile)

    return profile_to_read(profile)