"""Reliability service for tracking user reliability."""

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.reliability import Reliability
from app.models.user import User


def get_or_create_reliability(user_id: int, session: Session) -> Reliability:
    """Get existing reliability record or create one."""
    reliability = session.exec(
        select(Reliability).where(Reliability.user_id == user_id)
    ).first()

    if not reliability:
        # Validate user exists
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        reliability = Reliability(
            user_id=user_id,
            completed_circles=0,
            no_shows=0,
            reports_received=0,
            reliability_score=5.0,
        )
        session.add(reliability)
        session.commit()
        session.refresh(reliability)

    return reliability


def record_attendance(user_id: int, attendance_status: str, session: Session) -> Reliability:
    """
    Record attendance and update reliability score.
    
    attended: +completed_circles, reliability_score += 0.2 (max 5.0)
    no_show: +no_shows, reliability_score -= 0.5 (min 1.0)
    """
    reliability = get_or_create_reliability(user_id, session)

    if attendance_status == "attended":
        reliability.completed_circles += 1
        reliability.reliability_score = min(5.0, reliability.reliability_score + 0.2)

    elif attendance_status == "no_show":
        reliability.no_shows += 1
        reliability.reliability_score = max(1.0, reliability.reliability_score - 0.5)

    session.add(reliability)
    session.commit()
    session.refresh(reliability)
    return reliability


def record_report(user_id: int, session: Session) -> Reliability:
    """
    Record a report about a user and update reliability score.
    
    reliability_score -= 0.3 (min 1.0)
    """
    reliability = get_or_create_reliability(user_id, session)

    reliability.reports_received += 1
    reliability.reliability_score = max(1.0, reliability.reliability_score - 0.3)

    session.add(reliability)
    session.commit()
    session.refresh(reliability)
    return reliability


def get_user_reliability(user_id: int, session: Session) -> Reliability:
    """Get reliability record for a user."""
    return get_or_create_reliability(user_id, session)
