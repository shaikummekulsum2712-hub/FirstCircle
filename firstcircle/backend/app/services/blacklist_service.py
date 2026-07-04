"""Soft blacklist service."""

from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.soft_blacklist import SoftBlacklist
from app.models.user import User


def create_blacklist_entries(
    user_id: int,
    blocked_user_ids: list[int],
    reason: str,
    expires_days: int = 90,
    session: Session = None,
) -> list[SoftBlacklist]:
    """Create blacklist entries for a user blocking multiple users."""
    # Validate user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    blacklist_entries = []
    expires_at = datetime.utcnow() + timedelta(days=expires_days)

    for blocked_id in blocked_user_ids:
        # Validate blocked user exists
        blocked_user = session.get(User, blocked_id)
        if not blocked_user:
            continue

        # Check if already blacklisted
        existing = session.exec(
            select(SoftBlacklist).where(
                SoftBlacklist.user_id == user_id,
                SoftBlacklist.blocked_user_id == blocked_id,
            )
        ).first()

        if not existing:
            entry = SoftBlacklist(
                user_id=user_id,
                blocked_user_id=blocked_id,
                reason=reason,
                expires_at=expires_at,
            )
            session.add(entry)
            blacklist_entries.append(entry)

    session.commit()
    return blacklist_entries


def is_blacklisted(user_id: int, checked_user_id: int, session: Session) -> bool:
    """Check if user_id has checked_user_id blacklisted."""
    entry = session.exec(
        select(SoftBlacklist).where(
            SoftBlacklist.user_id == user_id,
            SoftBlacklist.blocked_user_id == checked_user_id,
        )
    ).first()

    if not entry:
        return False

    # Check expiry
    if entry.expires_at and entry.expires_at < datetime.utcnow():
        session.delete(entry)
        session.commit()
        return False

    return True


def get_user_blacklist(user_id: int, session: Session) -> list[SoftBlacklist]:
    """Get all users blacklisted by a user."""
    entries = session.exec(
        select(SoftBlacklist).where(SoftBlacklist.user_id == user_id)
    ).all()

    # Remove expired entries
    active_entries = []
    for entry in entries:
        if entry.expires_at and entry.expires_at < datetime.utcnow():
            session.delete(entry)
        else:
            active_entries.append(entry)

    session.commit()
    return active_entries
