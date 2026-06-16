from sqlalchemy.orm import Session
from ..models.profile import Profile
from ..models.reliability import ReliabilityHistory

def update_user_reliability(db: Session, profile_id: int, event_type: str, delta: float):
    """
    Applies reliability score updates to a profile, caps it at 100.0, and records history.
    """
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if profile:
        # Update profile reliability score
        new_score = profile.reliability_score + delta
        # Cap score between 0.0 and 100.0
        profile.reliability_score = max(0.0, min(100.0, new_score))

        # Log history event
        history_entry = ReliabilityHistory(
            profile_id=profile_id,
            event_type=event_type,
            delta=delta
        )
        db.add(history_entry)
        db.commit()
