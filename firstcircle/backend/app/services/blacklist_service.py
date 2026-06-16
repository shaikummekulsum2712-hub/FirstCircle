from sqlalchemy.orm import Session
from ..models.soft_blacklist import SoftBlacklist

def add_user_to_blacklist(db: Session, user_profile_id: int, target_profile_id: int) -> SoftBlacklist:
    existing = db.query(SoftBlacklist).filter(
        SoftBlacklist.user_id == user_profile_id,
        SoftBlacklist.blacklisted_user_id == target_profile_id
    ).first()
    
    if existing:
        return existing
        
    entry = SoftBlacklist(user_id=user_profile_id, blacklisted_user_id=target_profile_id)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def is_blacklisted_pair(db: Session, user_id_a: int, user_id_b: int) -> bool:
    count = db.query(SoftBlacklist).filter(
        (SoftBlacklist.user_id == user_id_a) & (SoftBlacklist.blacklisted_user_id == user_id_b) |
        (SoftBlacklist.user_id == user_id_b) & (SoftBlacklist.blacklisted_user_id == user_id_a)
    ).count()
    return count > 0
