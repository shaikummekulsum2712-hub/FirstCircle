from sqlalchemy.orm import Session
from typing import List
from ..models.profile import Profile
from ..models.free_slot import FreeSlot
from ..schemas.profile_schema import ProfileUpdate, FreeSlotCreate
from ..utils.validators import validate_interests_string, validate_bio_length

def get_profile_by_user_id(db: Session, user_id: int) -> Profile:
    return db.query(Profile).filter(Profile.user_id == user_id).first()

def update_profile(db: Session, profile: Profile, updates: ProfileUpdate) -> Profile:
    validate_bio_length(updates.bio)
    validate_interests_string(updates.interests)

    profile.display_name = updates.display_name
    profile.bio = updates.bio
    profile.age = updates.age
    profile.gender = updates.gender
    profile.interests = updates.interests
    if updates.comforts:
        profile.comforts = updates.comforts
        
    db.commit()
    db.refresh(profile)
    return profile

def set_profile_slots(db: Session, profile_id: int, slots: List[FreeSlotCreate]) -> List[FreeSlot]:
    # Delete existing slots first
    db.query(FreeSlot).filter(FreeSlot.profile_id == profile_id).delete()
    
    # Insert new slots
    db_slots = []
    for s in slots:
        db_slot = FreeSlot(
            profile_id=profile_id,
            day_of_week=s.day_of_week,
            start_time=s.start_time,
            end_time=s.end_time
        )
        db.add(db_slot)
        db_slots.append(db_slot)
        
    db.commit()
    return db_slots

def get_profile_slots(db: Session, profile_id: int) -> List[FreeSlot]:
    return db.query(FreeSlot).filter(FreeSlot.profile_id == profile_id).all()
